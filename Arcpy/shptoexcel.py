#coding=utf-8
import arcpy
from arcpy import env
import xlrd
import os
import time
import glob

'''
@des：将shp文件保存成excel文件  
'''
# 遍历文件夹
env.workspace = 'C:\Users\DSH\Documents\ArcGIS'
shp_list = glob.glob('*.shp')
#shp_list = ['1clip.shp']
print('总共发现%s个shp文件' % len(shp_list))
for shp in shp_list:
    savepath = 'E:' + u'\研一\项目\中山公交' + '\zhongshan\zhongshan\database\\result'
    # Set local variables
    in_table = shp
    out_xls = savepath+'\\'+shp.replace('clip.shp','re.xls')

    # Execute TableToExcel
    arcpy.TableToExcel_conversion(in_table, out_xls)
    print u'%s文件已完成'%shp
