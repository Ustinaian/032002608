import os
import asyncio
from asyncio import sleep
import random

from pyppeteer import launcher
# 在导入 launch 之前 把 --enable-automation 禁用 防止监测webdriver
launcher.DEFAULT_ARGS.remove("--enable-automation")

from pyppeteer import launch
from bs4 import BeautifulSoup


def sleep_time():
    return 3


async def pyppteer_fetchUrl(url):
    browser = await launch({'dumpio': True, 'autoClose': True})
    page = await browser.newPage()
    # 绕过反爬机制
    await page.evaluateOnNewDocument('() =>{ Object.defineProperties(navigator,''{ webdriver:{ get: () => false } }) }')
    # 伪装成浏览器
    await page.setUserAgent('Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Mobile Safari/537.36 Edg/105.0.1343.27')

    # await sleep(sleep_time())
    await page.goto(url)
    tasks = [asyncio.create_task(page.waitForNavigation())]
    await asyncio.wait(tasks)
    str = await page.content()
    await browser.close()
    return str


def fetchUrl(url):
    return asyncio.get_event_loop().run_until_complete(pyppteer_fetchUrl(url))


def getPageUrl():
    for page in range(1, 42):
        if page == 1:
            yield 'http://www.nhc.gov.cn/xcs/yqtb/list_gzbd.shtml'
        else:
            url = 'http://www.nhc.gov.cn/xcs/yqtb/list_gzbd_' + str(page) + '.shtml'
            yield url


def getTitleUrl(html):
    bsobj = BeautifulSoup(html, 'html.parser')
    titleList = bsobj.find('div', attrs={"class": "list"}).ul.find_all("li")
    for item in titleList:
        link = "http://www.nhc.gov.cn" + item.a["href"]
        title = item.a["title"]
        date = item.span.text
        yield title, link, date


def getContent(html):
    bsobj = BeautifulSoup(html, 'html.parser')
    cnt = bsobj.find('div', attrs={"id": "xw_box"}).find_all("p")
    s = ""
    if cnt:
        for item in cnt:
            s += item.text
        return s

    return "爬取失败！"


def saveFile(path, filename, content):
    if not os.path.exists(path):
        os.makedirs(path)

    # 保存文件
    with open(path + filename + '.txt', 'w', encoding='utf-8') as f:
        f.write(content)


if __name__ == "__main__":
    for url in getPageUrl():
        s = fetchUrl(url)
        for title, link, date in getTitleUrl(s):
            print(title)
            # 如果日期在1月21日之前，则直接退出
            mon = int(date.split("-")[1])
            day = int(date.split("-")[2])

            html = fetchUrl(link)
            content = getContent(html)
            # print(content)
            saveFile("D:/郭君濠/软件工程/第一次编程作业/疫情数据/", date, content)
            # print("-----" * 20)
