# -*- coding: utf-8 -*-
from __future__ import division
import csv

with open('validate2.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    column1 = [row for row in reader]
mannual = [i[0] for i in column1]
machine = [i[1] for i in column1]
tp = 0
fp = 0
fn = 0
tn = 0
for j in range(0, mannual.__len__()):
    if mannual[j] == '1' and machine[j] == '1':
        tp = tp + 1
    if mannual[j] == '0' and machine[j] == '1':
        fp = fp + 1
    if mannual[j] == '1' and machine[j] == '0':
        fn = fn + 1
    if mannual[j] == '0' and machine[j] == '0':
        tn = tn + 1
print 'TP=%s' % tp
print 'FP=%s' % fp
print 'FN=%s' % fn
print 'TN=%s' % tn
P = tp / (tp + fp)
R = tp / (tp + fn)
F1 = 2 * P * R / (P + R)
print  'Percision=%.5f' % P
print  'Recall=%.5f' % R
print  'F-Score=%.5f' % F1
