import re
import os
import xlwt


# 写入新增确诊和新增无症状数据
def save_data0(wb, ws, data1, data2, filename):
    col1 = ['地区', '新增确诊', '新增无症状']
    for j in range(0, 3):
        ws.write(0, j, col1[j])

    ws.write(1, 0, '中国大陆')
    ws.write(1, 1, data1)
    ws.write(1, 2, data2)


# 提取本土新增确诊和新增无症状数据
def readfile0(path, filename):
    with open(path + '/' + filename, 'r', encoding='utf-8') as f:
        str_data = f.read()
        # 提取新增确诊
        data_ml1 = re.findall(r"31个省（自治区、直辖市）和新疆生产建设兵团报告新增确诊病例(.+?)例", str_data)
        # 提取新增无症状
        data_ml2 = re.findall(r"31个省（自治区、直辖市）和新疆生产建设兵团报告新增无症状感染者(.+?)例", str_data)
        # 将数据存入excel
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('数据汇总', cell_overwrite_ok=True)
        save_data0(workbook, worksheet, data_ml1, data_ml2, filename)
        name = os.path.splitext(filename)[0]
        # 将excel表格保存起来
        workbook.save('D:/郭君濠/软件工程/第一次编程作业/提取数据/本土新增数据/' + name + '.xlsx')


# 写入各省新增确诊数据
def save_data1(ws, wb, i, area, data, filename):
    ws.write(i, 0, area)
    ws.write(i, 1, data)


# 提取各省新增确诊数据
def readfile1(path, filename):
    with open(path + '/' + filename, 'r', encoding='utf-8') as f:
        str_data = f.read()
        # 提取本土病例的一整段话
        try:
            str_data_p = re.findall(r"本土病例(.+?)），含", str_data)[0]
        except IndexError:
            return
        # 提取新增确诊地区名称
        data_p_all = re.findall('[\u4e00-\u9fa5]+', str_data_p)
        data_p_all.pop(0)

        # 提取新增确诊数据
        data_num = re.findall(r"\d+\.?\d*", str_data_p)
        data_num.pop(0)

        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('数据汇总')

        # 填入新增确诊标题
        worksheet.write(0, 0, '地区')
        worksheet.write(0, 1, '新增确诊')

        # 将新增确诊数据填入excel表格
        flag = 1
        count = 0
        for area in data_p_all:
            if flag == 0:
                flag = 1
                continue
            else:
                flag = 0
                # 将地区名称以及数据存入excel
                if len(data_num) <= 0:
                    return
                save_data1(worksheet, workbook, count+1, area, data_num[count], filename)
                if count >= len(data_num)-1:
                    break
                count += 1

        name = os.path.splitext(filename)[0]
        # 将新增确诊excel表格保存起来
        workbook.save('D:/郭君濠/软件工程/第一次编程作业/提取数据/新增确诊数据/' + name + '.xlsx')


# 存入各省新增无症状数据
def save_data2(ws, wb, i, area, data, filename):
    ws.write(i, 0, area)
    ws.write(i, 1, data)


# 提取各省新增无症状数据
def readfile2(path, filename):
    with open(path + '/' + filename, 'r', encoding='utf-8') as f:
        str_data = f.read()
        # 提取无症状病例的一整段话
        try:
            str_data_p2 = re.findall(r"本土[0-9]+例（.*?）", str_data)[0]
        except IndexError:
            return

        # 提取新增无症状地区
        data_p_all2 = re.findall('[\u4e00-\u9fa5]+', str_data_p2)
        data_p_all2.pop(0)
        data_p_all2.pop(0)

        # 提取新增无症状数据
        data_num2 = re.findall(r"\d+\.?\d*", str_data_p2)
        data_num2.pop(0)

        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('数据汇总')

        # 填入新增无症状标题
        worksheet.write(0, 0, '地区')
        worksheet.write(0, 1, '新增无症状')

        # 将新增无症状数据填入excel表格
        flag = 1
        count = 0
        for area in data_p_all2:
            if flag == 0:
                flag = 1
                continue
            else:
                flag = 0
                # 将地区名称以及数据存入excel
                if len(data_num2) <= 0:
                    return
                save_data2(worksheet, workbook, count+1, area, data_num2[count], filename)
                if count >= len(data_num2) - 1:
                    break
                count += 1

        name = os.path.splitext(filename)[0]
        # 将新增无症状excel表格保存起来
        workbook.save('D:/郭君濠/软件工程/第一次编程作业/提取数据/新增无症状数据/' + name + '.xlsx')


# 提取港澳台累计确诊数据
def readfile3(path, filename):
    with open(path + '/' + filename, 'r', encoding='utf-8') as f:
        str_data = f.read()
        # 提取港澳台的数据
        data0 = re.findall(r"香港特别行政区(.+?)例", str_data)
        data1 = re.findall(r"澳门特别行政区(.+?)例", str_data)
        data2 = re.findall(r"台湾地区(.+?)例", str_data)

        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('数据汇总')
        # 将港澳台数据写入excel表格
        worksheet.write(0, 0, '地区')
        worksheet.write(0, 1, '累计确诊病例')
        worksheet.write(1, 0, '香港')
        worksheet.write(1, 1, data0)
        worksheet.write(2, 0, '澳门')
        worksheet.write(2, 1, data1)
        worksheet.write(3, 0, '台湾')
        worksheet.write(3, 1, data2)
        # 将港澳台excel表格保存起来
        name = os.path.splitext(filename)[0]
        workbook.save('D:/郭君濠/软件工程/第一次编程作业/提取数据/港澳台累计确诊/' + name + '.xlsx')


if __name__ == "__main__":
    spath = 'D:/郭君濠/软件工程/第一次编程作业/爬取疫情数据/疫情数据'
    # 获取文件名列表
    files = os.listdir(spath)
    # 获取文件名

    for file in files:
        readfile0(spath, file)
        readfile1(spath, file)
        readfile2(spath, file)
        readfile3(spath, file)
        basename = os.path.splitext(file)[0]
        print(basename)

