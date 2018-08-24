# -*- coding: utf-8 -*-

'''
@des:模拟退火算法求解函数最小值问题
'''
import numpy as np
from matplotlib import pyplot as plt

def inputFunction(x):
    return (x-2)*(x+3)*(x+8)*(x-9)

#模拟退火算法
def SA(inputFunction,k = 1,T = 1000,alpha = 0.95,iterL=100):
    #初始化
    minT = -np.inf #温度下限
    x_old=10*(2*np.random.rand()-1)
    x_new=x_old
    epoch=0
    while epoch < iterL:
        if x_old < minT:
            break
        x_new = x_old+(2*np.random.rand()-1)
        deltax=inputFunction(x_new)-inputFunction(x_old)
        if deltax<0:
            x_old=x_new
        else:
            pc=np.exp(-deltax/(k*T))
            if np.random.rand()<pc:
                x_old=x_new
        T=alpha*T
        epoch+=1
        print(epoch)
    return x_old,inputFunction(x_old)

x_re,y_re=SA(inputFunction)
x=np.linspace(-10,10,200)
y=(x-2)*(x+3)*(x+8)*(x-9)
plt.plot(x,y,c='b')
plt.scatter([x_re],[y_re],c='r')
plt.show()