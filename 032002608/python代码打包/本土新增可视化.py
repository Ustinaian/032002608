import os
import xlrd
from pyecharts.charts import Bar
from pyecharts import options as opts

def visualize(filename):
    basename = os.path.splitext(filename)[0]
    data = xlrd.open_workbook(filename)

    table = data.sheets()[0]

    areas = []
    datas = []
    datas2 = []

    for i in range(1, table.nrows):
        # 把第几行拿出来作为一个列表
        a = table.row_values(i)
        area = a[0]
        areas.append(area)
        da = a[1]
        datas.append(da)
        da2 = a[2]
        datas2.append(da2)

    # 创建一个柱状图对象
    bar = Bar()
    # 设置x轴
    bar.add_xaxis(areas)
    # 设置y轴和图标名
    y_title = table.row_values(0)
    bar.add_yaxis(y_title[1], datas)
    bar.add_yaxis(y_title[2], datas2)
    # 添加options
    bar.set_global_opts(title_opts=opts.TitleOpts(title=basename))

    # 输出html文件来显示柱状图
    bar.render('D:/郭君濠/软件工程/第一次编程作业/可视化/柱状图/本土新增数据柱状图/' + basename + '.html')
    print(basename)

if __name__ == '__main__':
    spath = 'D:/郭君濠/软件工程/第一次编程作业/提取数据/本土新增数据'
    files = os.listdir(spath)
    for file in files:
        visualize(file)

