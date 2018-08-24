#coding=utf-8
import arcpy
from arcpy import env
import xlrd
import os
import time
import glob

'''
@des：利用arcpy将excel表格转化为shp文件
'''
# 遍历文件夹
env.workspace = 'C:\Users\DSH\Documents\ArcGIS'
excel_list = glob.glob('*.xlsx')
# excel_list = ['1.xlsx']
print('总共发现%s个excel文件' % len(excel_list))
for table in excel_list:
    savepath = 'E:' + u'\研一\项目\中山公交' + '\zhongshan\zhongshan\database\pointshp'
    name = str(table).replace('.xlsx', '')
    # 利用表名，根据CreateFeatureclass_management（）函数新建一个点要素类
    if arcpy.Exists(savepath + '\\' + name + '.shp') == False:
        arcpy.CreateFeatureclass_management(savepath, name, 'POINT', '', '', '', 'WGS 1984.prj')
    else:
        pass
    # 根据表路径，读取表里的内容
    data = xlrd.open_workbook(table)
    sh = data.sheets()[0]
    try:
        arcpy.AddField_management(savepath + '\\' + name + '.shp', 'STOPNAME', 'TEXT')
        arcpy.AddField_management(savepath + '\\' + name + '.shp', 'STOPORDER', 'FLOAT')
        arcpy.AddField_management(savepath + '\\' + name + '.shp', 'LONGITUDE', 'FLOAT')
        arcpy.AddField_management(savepath + '\\' + name + '.shp', 'LATITUDE', 'FLOAT')
        arcpy.AddField_management(savepath + '\\' + name + '.shp', 'ROUTENAME', 'TEXT')
        rownum = sh.nrows  # 获得表格的行数
        # 接下来读取Excle表格的内容，利用插入游标给上面新建的点要素类插入数据（row)
        Insercur = arcpy.InsertCursor(savepath + '\\' + name + '.shp')
        for r in range(1, rownum):
            newpnt = arcpy.Point()  # 新建一个点
            # 获得点的xy坐标并赋值给点的XY属性
            # sh.cell(r,c).value，这里的r,c索引要根据你自己表格的格式设置
            newpnt.X = sh.cell(r, 10).value
            newpnt.Y = sh.cell(r, 11).value
            pointGeo = arcpy.PointGeometry(newpnt)
            newrow = Insercur.newRow()  # 插入游标新建行row
            newrow.shape = pointGeo
            newrow.setValue('STOPNAME', sh.cell(r, 1).value)
            t = sh.cell(r, 8).value
            newrow.setValue('STOPORDER', sh.cell(r, 8).value)
            newrow.setValue('LONGITUDE', sh.cell(r, 10).value)
            newrow.setValue('LATITUDE', sh.cell(r, 11).value)
            newrow.setValue('ROUTENAME', sh.cell(r, 17).value)
            Insercur.insertRow(newrow)  # 插入row
    except Exception as e:
        print e
    print u'%s文件已完成'%table
