import os
import asyncio

from pyppeteer import launcher
# 在导入 launch 之前 把 --enable-automation 禁用 防止监测webdriver
launcher.DEFAULT_ARGS.remove("--enable-automation")

from pyppeteer import launch
from bs4 import BeautifulSoup


# 将 pyppeteer 的操作封装成 fetchurl 函数，用于发起网络请求，获取网页源码
async def pyppteer_fetchUrl(url):
    browser = await launch({'dumpio': True, 'autoClose': True})
    page = await browser.newPage()
    # 绕过反爬机制
    await page.evaluateOnNewDocument('() =>{ Object.defineProperties(navigator,''{ webdriver:{ get: () => false } }) }')
    # 伪装成浏览器
    await page.setUserAgent('Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, '
                            'like Gecko) Chrome/105.0.0.0 Mobile Safari/537.36 Edg/105.0.1343.27')

    await page.goto(url)
    tasks = [asyncio.create_task(page.waitForNavigation())]
    await asyncio.wait(tasks)
    str = await page.content()
    await browser.close()
    return str


def fetchurl(url):
    return asyncio.get_event_loop().run_until_complete(pyppteer_fetchUrl(url))


# 通过 getpageurl 函数构造每一页的 URL 链接
def getpageurl():
    for page in range(1, 2):
        if page == 1:
            yield 'http://www.nhc.gov.cn/xcs/yqtb/list_gzbd.shtml'
        else:
            url = 'http://www.nhc.gov.cn/xcs/yqtb/list_gzbd_' + str(page) + '.shtml'
            yield url


# 通过 getTitleUrl 函数，获取某一页的文章列表中的每一篇文章的标题，链接，和发布日期。
def getTitleUrl(html):
    b = BeautifulSoup(html, 'html.parser')
    titleList = b.find('div', attrs={"class": "list"}).ul.find_all("li")
    for item in titleList:
        link = "http://www.nhc.gov.cn" + item.a["href"]
        title = item.a["title"]
        date = item.span.text
        yield title, link, date


# 通过 getContent 函数，获取某一篇文章的正文内容。（如果没有获取到正文部分，则返回 “爬取失败”）
def getContent(html):
    bsobj = BeautifulSoup(html, 'html.parser')
    cnt = bsobj.find('div', attrs={"id": "xw_box"}).find_all("p")
    s = ""
    if cnt:
        for item in cnt:
            s += item.text
        return s
    return "爬取失败！"


# 通过 savefile 函数，可以将爬取到的数据保存在本地的 txt 文档里
def savefile(path, filename, con):
    if not os.path.exists(path):
        os.makedirs(path)

    # 保存文件
    with open(path + filename + '.txt', 'w', encoding='utf-8') as f:
        f.write(con)


if __name__ == "__main__":
    for url in getpageurl():
        s = fetchurl(url)
        for title, link, date in getTitleUrl(s):
            print(title)
            html = fetchurl(link)
            content = getContent(html)
            savefile("D:/郭君濠/软件工程/第一次编程作业/疫情数据/", date, content)
