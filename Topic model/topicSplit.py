# -*- coding: utf-8 -*-
import lda
import collections
import numpy as np
import codecs
import csv
import xlwt
import pandas as pd

def readcsv(strFile):
    with open(strFile, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        column1 = [row for row in reader]
        time = [i[0] for i in column1[1:]]
        lat = [i[1] for i in column1[1:]]
        lon = [i[2] for i in column1[1:]]
        content = [i[3] for i in column1[1:]]
        topicID = [i[4] for i in column1[1:]]
    return time,lat,lon,content, topicID
[time,lat,lon,content, topicID]=readcsv('result_40topics.csv')
wb=xlwt.Workbook(encoding='utf8')
num=len(content)
for i in range(0,40):
    rowNum = 1
    ws = wb.add_sheet(str(i))
    ws.write(rowNum, 0, 'time')
    ws.write(rowNum, 0, 'lat')
    ws.write(rowNum, 0, 'lon')
    ws.write(rowNum, 0, 'text')
    ws.write(rowNum, 0, 'topic')
    for j in range(0, num):
        if topicID[j] == str(i):
            ws.write(rowNum, 0, time[j])
            ws.write(rowNum, 1, lat[j])
            ws.write(rowNum, 2, lon[j])
            ws.write(rowNum, 3, content[j].decode('GBK', 'ignore').encode('utf8', 'ignore'))
            ws.write(rowNum, 4, topicID[j])
            rowNum = rowNum + 1
wb.save('result_topic40.xls')

