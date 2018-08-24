# -*- coding: utf-8 -*-
import lda
import collections
import numpy as np
import csv
import jieba
import codecs
import re
import os


def read_tingyongci():
    path = "123.txt"   #停用词分析
    stop_words = []
    csv_reader = codecs.open(path,"r", "gbk")
    for row in csv_reader:
        row = row.strip( '\r\n' ).encode("utf-8")
        stop_words.append(row)
    return stop_words
stop_words = read_tingyongci()

# 将utf8的列表转换成unicode
def changeListCode(b):
    a = []
    for i in b:
            try:
                i1 = i.decode('GB18030').encode('utf-8')
                a.append(i.decode('GB18030').encode('utf-8'))
            except:
                a.append(i)
    return a

def readtrain():
    with open('train.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile)
        column1 = [row for row in reader]
    content_train = [i[0] for i in column1[0:]]
    train = changeListCode(content_train)
    print '有 %s 条句子' % len(content_train)
    return train

# 对列表进行分词并用空格连接
def segmentWord(cont):
    c = []
    patt1 = re.compile(r'\[.*?\]')
    for i in cont:
        s=[]
        line1 = re.sub(patt1, '', i)
        wordList = jieba.cut(line1)
        for i in wordList:
            if i >= u'\u4e00' and i <= u'\u9fa5':

                if i.encode('utf8') in stop_words:
                    pass
                else:
                    s.append(i.encode('utf8'))
        b=" ".join(s)
        c.append(b)
    return c

stopwords = read_tingyongci()
train = readtrain()
content = segmentWord(train)

f=open("cutWordsFile.txt",'w')
for i in range(0,content.__len__()-1):
    f.write(content[i])
    f.write('\n')
f.write(content[content.__len__()-1])
f.close()