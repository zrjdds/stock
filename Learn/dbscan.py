#coding=utf-8

from sklearn import datasets
import pandas  as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import DBSCAN

def epsilon(data, MinPts):
    '''计算最佳半径
    input:  data(mat):训练数据
            MinPts(int):半径内的数据点的个数
    output: eps(float):半径
    '''
    m, n = np.shape(data)
    xMax = np.max(data, 0)
    xMin = np.min(data, 0)
    eps = ((np.prod(xMax - xMin) * MinPts * math.gamma(0.5 * n + 1)) / (m * math.sqrt(math.pi ** n))) ** (1.0 / n)
    return eps


if __name__ == '__main__':
    iris = datasets.load_iris()
    iris_x = iris.data[:, 2:4]  # z只取后两个维度

    eps = epsilon()

    estimator = DBSCAN(eps=0.5, min_samples=3)  # 构造聚类器,一个参数是半径，一个是密度
    estimator.fit(iris_x)
    label_pred = estimator.labels_  # 获取聚类标签
    print(type(label_pred))
    print(iris_x)

    # 绘制k-means结果
    x0 = iris_x[label_pred == 0]
    x1 = iris_x[label_pred == 1]
    plt.scatter(x0[:, 0], x0[:, 1], c="red", marker='o', label='label0')
    plt.scatter(x1[:, 0], x1[:, 1], c="green", marker='*', label='label1')
    plt.show()
