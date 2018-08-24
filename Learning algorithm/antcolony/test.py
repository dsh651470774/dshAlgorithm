# encoding: utf-8
from Tkinter import *
import matplotlib
import numpy as np
import random

indistMat=np.mat([[0,2,10,8,3],[1,0,2,5,7],[9,1,0,3,6],[10,4,3,0,2],[2,7,5,1,0]])
citylabels=['A','B','C','D','E']


def AntColony(distMat, citylabels):
    m = distMat.shape[0]  # 城市个数
    antNum = m  # 蚂蚁数量
    alpha = 1  # 信息素重要程度因子
    beta = 1  # 启发函数重要程度因子
    rho = 0.5  # 信息素的挥发速度
    Q = 100  # 残留信息素浓度
    nMat = np.divide(1.0, distMat)  # 启发因子矩阵
    maxiter = 200  # 最大迭代次数
    iterNum = 0
    citylist = range(m)
    # 初始化信息素矩阵
    taoMat = np.mat(np.ones((m, m))) * 2
    deltataoMat = np.mat(np.zeros((m, m)))
    lengthbest = np.inf  # =最佳路径长度
    pathbest = np.mat(np.zeros((1, m)))  # 最佳路径
    while (iterNum < maxiter):
        routeMat = np.mat(np.zeros((antNum, m + 1), dtype=int))
        # 存储距离
        L = np.array([0.0] * antNum)
        for antind in range(antNum):
            # 假设第i只蚂蚁从第i个城市出发,初始化禁忌表
            routeMat[antind, 0]=antind
            tabuList = [antind]
            oldcity = antind
            # 中间总共需要选择m-1次
            for step in range(m - 1):
                print oldcity
                # 计算下一个城市的概率
                p0 = np.array([0.0] * m)
                for newcity in citylist:
                    if newcity in tabuList:
                        continue
                    p0[newcity] = taoMat[oldcity, newcity] ** alpha * nMat[oldcity, newcity] ** beta
                p = p0 / float(np.sum(p0))
                # 轮盘赌选择
                randomchoose = random.random()
                psum = 0
                choosecity = -1
                while (psum < randomchoose):
                    choosecity += 1
                    psum += p[choosecity]
                # 记录下该城市,并增加禁忌表,计算长度
                routeMat[antind, step + 1] = choosecity
                tabuList.append(choosecity)
                L[antind] += distMat[oldcity, choosecity]
                oldcity = choosecity
            # 计算最后城市回到原点的距离
            routeMat[antind, m] = antind
            L[antind] += distMat[oldcity, antind]
            # 计算信息素增量矩阵
            for i in range(m):
                deltataoMat[routeMat[antind, i], routeMat[antind, i + 1]] += float(Q) / L[antind]
                deltataoMat[routeMat[antind, i + 1], routeMat[antind, i]] += float(Q) / L[antind]

        # 更新最优路线以及最短距离
        if L.min() < lengthbest:
            pathbest = routeMat[L.argmin(), :]
            lengthbest = L.min()
        # 更新信息素
        taoMat = (1 - rho) * taoMat + deltataoMat
        iterNum += 1
        bestRoute = []
        for i in range(pathbest.shape[1]):
            bestRoute.append(citylabels[pathbest[0, i]])
    return bestRoute, lengthbest

print AntColony(indistMat,citylabels)