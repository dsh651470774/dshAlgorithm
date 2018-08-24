#coding=utf-8
import arcpy
from arcpy import env
import xlrd
import os
import time
import glob

'''
@des：利用arcpy将点集转换成线
'''
# 遍历文件夹
env.workspace = 'C:\Users\DSH\Documents\ArcGIS'
shp_list = glob.glob('*.shp')
#shp_list = ['1.shp']
print('总共发现%s个shp文件' % len(shp_list))
for shp in shp_list:
    savepath = 'E:' + u'\研一\项目\中山公交' + '\zhongshan\zhongshan\database\lineshp'
    inFeatures = shp
    outFeatures = savepath+'\\'+shp.replace('.shp','')+'line.shp'
    lineField = "ROUTENAME"
    sortField = "STOPORDER"
    # Execute PointsToLine
    arcpy.PointsToLine_management(inFeatures, outFeatures, lineField, sortField)
    print u'%s文件已完成'%shp
