#coding=utf-8
import arcpy
from arcpy import env
import xlrd
import os
import time
import glob

'''
@des：裁剪图层   
'''
# 遍历文件夹
env.workspace = 'C:\Users\DSH\Documents\ArcGIS'
shp_list = glob.glob('*.shp')
#shp_list = ['1cp.shp']
print('总共发现%s个shp文件' % len(shp_list))
for shp in shp_list:
    savepath = 'E:' + u'\研一\项目\中山公交' + '\zhongshan\zhongshan\database\\clippoint'
    in_features = shp
    clip_features = 'E:' + u'\研一\项目\中山公交' + '\zhongshan\zhongshan\database\\buffershp'+'\\'+shp.replace('cp.shp','buffer.shp')
    out_feature_class = savepath+'\\'+shp.replace('cp.shp','clip.shp')
    xy_tolerance = ""
    # Execute Clip
    arcpy.Clip_analysis(in_features, clip_features, out_feature_class, xy_tolerance)
    print u'%s文件已完成'%shp
