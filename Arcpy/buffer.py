#coding=utf-8
import arcpy
from arcpy import env
import xlrd
import os
import time
import glob

'''
@des：按照距离建立缓冲区
'''
# 遍历文件夹
env.workspace = 'C:\Users\DSH\Documents\ArcGIS'
shp_list = glob.glob('*.shp')
#shp_list = ['1line.shp']
print('总共发现%s个shp文件' % len(shp_list))
for shp in shp_list:
    savepath = 'E:' + u'\研一\项目\中山公交' + '\zhongshan\zhongshan\database\\buffershp'
    # Buffer areas of impact around major roads
    roads = shp
    roadsBuffer = savepath+'\\'+shp.replace('line.shp','buffer.shp')
    distanceField = '500 meters'
    sideType = "FULL"
    endType = "ROUND"
    dissolveType = "LIST"
    arcpy.Buffer_analysis(roads, roadsBuffer, distanceField, sideType, endType, dissolveType)
    print u'%s文件已完成'%shp
