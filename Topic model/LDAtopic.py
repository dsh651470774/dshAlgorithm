# -*- coding: utf-8 -*-
import lda
import collections
import numpy as np
import codecs
import csv

def readtrain():
    with open('train.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile)
        column1 = [row for row in reader]
        train = [i[0] for i in column1[0:]]
    return train
#去重
cutWordsFile = 'cutWordsFile.txt'   #语料库文件，其内一行是一个已切好词的文本
wordSet = set()
for eachLine1 in codecs.open(cutWordsFile, 'r', 'utf8'):
    eachLine1=eachLine1.encode('utf-8')
    lineList1 = eachLine1.split(' ')
    for i in range(len(lineList1)):
        wordSet.add(lineList1[i].strip())
wordList = list(wordSet)

#生成词频矩阵，一行一个文本，一列一个词语，数值等于该词语在当前文本中出现的频次
# 矩阵行数=文本总数，矩阵列数=语料库去重后词语总数
#该矩阵是一个大的稀疏矩阵
wordMatrix = []
for eachLine2 in codecs.open(cutWordsFile, 'r', 'utf-8'):
    eachLine2 = eachLine2.encode('utf-8')
    docWords = eachLine2.strip().split(' ')
    dict1 = collections.Counter(docWords)
    key1 = list(dict1.keys())
    r1 = []
    for i in range(len(wordList)):
        if wordList[i] in key1:
            r1.append(dict1[wordList[i]])
        else:
            r1.append(0)
    wordMatrix.append(r1)
X = np.array(wordMatrix)    #词频矩阵

# 模型训练
model = lda.LDA(n_topics=40, n_iter=2000, random_state=1)
model.fit(X)
np.set_printoptions(threshold=np.inf)
# doc-topic分布
print('==================doc:topic==================')
doc_topic = model.doc_topic_
print(type(doc_topic))
print(doc_topic.shape)
# print(doc_topic)  # 一行为一个doc属于每个topic的概率，每行之和为1

# topic-word分布
n = 20
print('==================topic:word==================')
topic_word = model.topic_word_
print(type(topic_word))
print(topic_word.shape)
print(np.sort(topic_word)[:,:-10:-1])  # 一行对应一个topic，即每行是一个topic及该topic下词的概率分布，每行之和为1

# 每个topic内权重最高的20个词语

print('==================topic top' + str(n) + ' word==================')
for i, topic_dist in enumerate(topic_word):
    topic_words = np.array(wordList)[np.argsort(topic_dist)][:-(n + 1):-1]
    print('*Topic {}\n-{}'.format(i, ' '.join(topic_words)))

# 每篇文本最可能的topic
print('==================doc best topic==================')
txtNums = len(codecs.open(cutWordsFile, 'r', 'utf-8').readlines())  # 文本总数
for i in range(10):
    topic_most_pr = doc_topic[i].argmax()
    print('doc: {} ,best topic: {}'.format(i, topic_most_pr))

train = readtrain()
csvfile = file('result_40.csv', 'wb')
writer = csv.writer(csvfile)
for i in range(0,train.__len__()):
    writer.writerow([train[i],doc_topic[i].argmax()])


