# -*- coding: utf-8 -*-
import csv
import jieba
import codecs
import re
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
import xlwt
from sklearn import metrics
from sklearn.grid_search import GridSearchCV
from sklearn.naive_bayes import MultinomialNB



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
    content_train = [i[0] for i in column1[0:]] #第一列为文本内容，并去除列名
    content_train = changeListCode(content_train)
    opinion_train = [i[1] for i in column1[0:]] #第二列为类别，并去除列名
    print('训练集有 %s 条句子'% len(content_train))
    train = [content_train, opinion_train]
    return train

def readexam():
    with open('exam.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile)
        column1 = [row for row in reader]
    content_exam = [i[0] for i in column1[0:]] #第一列为文本内容，并去除列名
    print('测试集有 %s 条句子' % len(content_exam))
    return content_exam

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

# corpus = ["我 来到 北京 清华大学", "他 来到 了 网易 杭研 大厦", "小明 硕士 毕业 与 中国 科学院"]
stopwords = read_tingyongci()
train = readtrain()
data_exam = readexam()
exam = changeListCode(data_exam)
content = segmentWord(train[0])
opinion = train[1]
exam_content = segmentWord(exam)


# # 划分
train_content = content
train_opinion = opinion



# 计算权重
vectorizer = CountVectorizer()
tfidftransformer = TfidfTransformer()
tfidf = tfidftransformer.fit_transform(vectorizer.fit_transform(train_content))  # 先转换成词频矩阵，再计算TFIDF值
print(tfidf.shape)


# # 单独预测
word = vectorizer.get_feature_names()
weight = tfidf.toarray()
# 分类器
clf = MultinomialNB().fit(tfidf, opinion)
new_tfidf = tfidftransformer.transform(vectorizer.transform(exam_content))
predicted = clf.predict(new_tfidf)
exam_option=predicted
# print predicted
# #


# 训练和预测一体
# text_clf = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', SVC(C=0.99, kernel='linear'))])
# text_clf = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', MultinomialNB(alpha=1.0))])
# text_clf = text_clf.fit(train_content, train_opinion)
# predicted = text_clf.predict(exam_content)
# exam_option=predicted

csvfile = file('result_nb2.csv', 'wb')
writer = csv.writer(csvfile)
for i in range(0,exam.__len__()):
 writer.writerow([exam_option[i],data_exam[i]])

# 循环调参

# parameters = {'vect__max_df': (0.4, 0.5, 0.6, 0.7),'vect__max_features': (None, 5000, 10000, 15000),
#               'tfidf__use_idf': (True, False)}
# grid_search = GridSearchCV(text_clf, parameters, n_jobs=1, verbose=1)
# grid_search.fit(content, opinion)
# best_parameters = dict()
# best_parameters = grid_search.best_estimator_.get_params()
# for param_name in sorted(parameters.keys()):
#     print("\t%s: %r" % (param_name, best_parameters[param_name]))


