# -*- coding: utf-8 -*-
import csv
import jieba
import codecs
import re
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import xlwt
from sklearn import metrics
import matplotlib.pyplot as plt
import math
import jieba.posseg as pseg

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

def readexam():
    with open('all.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile)
        column1 = [row for row in reader]
    content_exam = [i[3] for i in column1[1:]] #第一列为文本内容，并去除列名
    print '测试集有 %s 条句子' % len(content_exam)
    return content_exam

# 对列表进行分词并用空格连接
def segmentWord(cont):
    c = []
    cixing = ['n', 'v' , 'vn','a','nr','nt','l','nz','ns','i','f','d','t','s','eng','an']
    patt1 = re.compile(r'\[.*?\]')
    for i in cont:
        s=[]
        line1 = re.sub(patt1, '', i)
        wordList = pseg.cut(line1)
        for i in wordList:
            if i.word >= u'\u4e00' and i.word <= u'\u9fa5':
                if i.word.encode('utf8') in stop_words:
                    pass
                else:
                    if i.flag in cixing:
                        s.append(i.word.encode('utf8'))
        b=" ".join(s)
        c.append(b)
    return c
def callog(X):
    return math.log(X+1)
def drawPWords(wordWeightList,splitNum=200):
    minVal=min(wordWeightList)
    maxVal=max(wordWeightList)
    stepVal=(maxVal-minVal)/float(splitNum)
    freqList=[0]*splitNum
    for i in range(len(wordWeightList)):
        if wordWeightList[i] >= minVal and wordWeightList[i] <= minVal + stepVal:
            freqList[0]+=1
            continue
        for j in range(1,splitNum):
            if wordWeightList[i] > minVal+j*stepVal and wordWeightList[i] <= minVal + (j+1)*stepVal:
                freqList[j] += 1
    X=range(1,splitNum+1)
    #画第一张图
    plt.subplot(121)
    plt.xlabel("TF-IDF")
    plt.ylabel("Frequance")
    plt.title("TF-IDF Explore")
    plt.bar(X, freqList)
    #画第二张图
    plt.subplot(122)
    plt.xlabel("log(TF-IDF bins)")
    plt.ylabel("log(Frequance)")
    plt.title("TF-IDF powerlaw Explore")
    plt.plot(map(callog,map(float,X)), map(callog,map(float,freqList)))
    plt.show()

# corpus = ["我 来到 北京 清华大学", "他 来到 了 网易 杭研 大厦", "小明 硕士 毕业 与 中国 科学院"]
stopwords = read_tingyongci()
data_exam = readexam()
exam = changeListCode(data_exam)
content = segmentWord(exam)
# 计算权重
vectorizer = CountVectorizer()
tfidftransformer = TfidfTransformer()
tfidf = tfidftransformer.fit_transform(vectorizer.fit_transform(content))  # 先转换成词频矩阵，再计算TFIDF值
print tfidf.shape
word=vectorizer.get_feature_names()#获取词袋模型中的所有词语
weight=tfidf.toarray()#将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
wordWeightList=[0]*len(word)
for i in range(len(weight)):#打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
    for j in range(len(word)):
        wordWeightList[j]+=weight[i][j]
#看下划分结果下的词频分布
#第一次划分
orderwords=np.argsort(-np.array(wordWeightList))
threshold=np.mean(np.array(wordWeightList))
wordList2=[]
wordWeightList2=[]
for i in range(len(wordWeightList)):
    if wordWeightList[orderwords[i]] < threshold:
        break
    wordList2.append(word[orderwords[i]])
    wordWeightList2.append(wordWeightList[orderwords[i]])
#第二次划分
orderwords2=np.argsort(-np.array(wordWeightList2))
threshold2=np.mean(np.array(wordWeightList2))
# wordList3=[]
# wordWeightList3=[]
# for i in range(len(wordWeightList2)):
#     if wordWeightList2[orderwords2[i]] < threshold2:
#         break
#     wordList3.append(wordList2[orderwords2[i]])
#     wordWeightList3.append(wordWeightList2[orderwords2[i]])
# print len(wordList3)
f = codecs.open("keywordsflag3.txt", "w", "utf-8")
for i in range(len(wordWeightList2)):
    if wordWeightList2[orderwords2[i]]<threshold2:
        break
    f.write(wordList2[orderwords2[i]])
    f.write('\n')
f.close()
# #第三次划分
# orderwords3=np.argsort(-np.array(wordWeightList3))
# threshold3=np.mean(np.array(wordWeightList3))
# wordList4=[]
# wordWeightList4=[]
# for i in range(len(wordWeightList3)):
#     if wordWeightList3[orderwords3[i]] < threshold3:
#         break
#     wordList4.append(wordList3[orderwords3[i]])
#     wordWeightList4.append(wordWeightList3[orderwords3[i]])
# print len(wordList4)
# drawPWords(wordWeightList4,200)