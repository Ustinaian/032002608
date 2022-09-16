import re
import os
import xlwt

list_p = ["北京", "天津", "上海", "重庆", "内蒙古", "新疆", "西藏", "宁夏", "广西", "黑龙江", "吉林", "辽宁", "河北", "河南", "山东",
          "山西", "甘肃", "陕西", "青海", "四川", "湖北", "安徽", "江苏", "浙江", "福建", "江西", "湖南", "贵州", "云南", "广东", "海南"]


def save_data(ws, data1, data2, filename):
    col1 = ['地区', '新增确诊', '新增无症状']
    for j in range(0, 3):
        ws.write(0, j, col1[j])

    ws.write(1, 0, '中国大陆')
    ws.write(1, 1, data1)
    ws.write(1, 2, data2)


def save_data2(ws, wb, i, area, data, filename):
    ws.write(i, 0, area)
    ws.write(i, 1, data)
    name = os.path.splitext(filename)[0]
    # 将excel表格保存起来
    wb.save('D:/郭君濠/软件工程/第一次编程作业/提取数据/数据/' + name + '.xlsx')


def readfile(path, filename):
    with open(path + '/' + filename, 'r', encoding='utf-8') as f:
        str_data = f.read()
        # 提取新增确诊
        data_ml1 = re.findall(r"31个省（自治区、直辖市）和新疆生产建设兵团报告新增确诊病例(.+?)例", str_data)
        # 提取新增无症状
        data_ml2 = re.findall(r"31个省（自治区、直辖市）和新疆生产建设兵团报告新增无症状感染者(.+?)例", str_data)
        # 将数据存入excel
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('数据汇总', cell_overwrite_ok=True)
        save_data(worksheet, data_ml1, data_ml2, filename)

        # 提取本土病例的一整段话
        try:
            str_data_p = re.findall(r"本土病例(.+?)），含", str_data)[0]
        except IndexError:
            return
        # 提取地区名称
        data_p_all = re.findall('[\u4e00-\u9fa5]+', str_data_p)
        data_p_all.pop(0)
        # 提取数据
        data_num = re.findall(r"\d+\.?\d*", str_data_p)
        data_num.pop(0)

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
                save_data2(worksheet, workbook, count+2, area, data_num[count], filename)
                if count >= len(data_num)-1:
                    break
                count += 1


if __name__ == "__main__":
    spath = 'D:/郭君濠/软件工程/第一次编程作业/爬取疫情数据/疫情数据'
    # 获取文件名列表
    files = os.listdir(spath)
    # 获取文件名

    for file in files:
        readfile(spath, file)
        basename = os.path.splitext(file)[0]

        print(basename)

