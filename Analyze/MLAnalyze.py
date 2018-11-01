#coding=utf-8

from Data import StockDataOperator
from Data import StockDataManager
from Analyze import BasicAnalyze
from Analyze.DimReduction import PCA
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import DBSCAN
import numpy as np
np.set_printoptions(threshold=np.inf)

import seaborn as sns
import pandas as pd

import math
import datetime

from GUI import PyQt5GUI

from matplotlib.font_manager import FontProperties
font_set = FontProperties(fname=r"C:\windows\fonts\simsun.ttc", size=12)

class MLAnalyze:
    def __init__(self):
        pass

    @staticmethod
    def lstm_price_forcast(stock_code):
        stock_data = StockDataManager.StockDataManager.load_stock_data_by_stock_code(stock_code)
        if stock_data is None:
            print("No data")

        if stock_data is not None:
            stock_close_list = []
            stock_date_list = []

            stock_data_len = len(stock_data)
            i = 0
            while i < stock_data_len:
                stock_close_list.append(stock_data[i][2])
                stock_date_list.append(stock_data[i][1])
                i = i + 1

        print(stock_close_list)

        PyQt5GUI.PyQt5GUI.only_instance.liu_stock_bottom_run_flag = False
        msg = '已完成代码为 %s 的股票LSTM股票收盘价预测分析' % stock_code
        PyQt5GUI.PyQt5GUI.only_instance.log_msg(msg)

    @staticmethod
    def stock_info_clustering():
        stock_info = StockDataManager.StockDataManager.load_stock_info()
        stock_count = len(stock_info)

        stock_numeric_orgin_data = np.zeros([stock_count, 18])
        stock_index_data = np.arange(0, stock_count)

        i = 0
        for stock in stock_info:
            stock_code = stock[0]  # 代码
            name = stock[1]  # 名称
            industry = stock[2]  # 所属行业
            area = stock[3]  # 地区
            pe = stock[4]  # 市盈率
            outstanding = stock[5]  # 流通股本
            totals = stock[6]  # 总股本
            totalAssets = stock[7]  # 总资产
            liquidAssets = stock[8]  # 流动资产
            fixedAssets = stock[9]  # 固定资产
            reserved = stock[10]  # 公积金
            reservedPerShare = stock[11]  # 每股公积金
            esp = stock[12]  # 每股收益
            bvps = stock[13]  # 每股净资
            pb = stock[14]  # 市净率
            timeToMarket = stock[15]  # 上市日期
            undp = stock[16]  # 未分配利润
            perundp = stock[17]  # 每股未分配
            rev = stock[18]  # 收入同比
            profit = stock[19]  # 利润同比
            gpr = stock[20]  # 毛利率
            npr = stock[21]  # 净利润率
            holders = stock[22]  # 股东人数

            stock_numeric_orgin_data[i, 0] = pe
            stock_numeric_orgin_data[i, 1] = outstanding
            stock_numeric_orgin_data[i, 2] = totals
            stock_numeric_orgin_data[i, 3] = totalAssets
            stock_numeric_orgin_data[i, 4] = liquidAssets
            stock_numeric_orgin_data[i, 5] = fixedAssets
            stock_numeric_orgin_data[i, 6] = reserved
            stock_numeric_orgin_data[i, 7] = reservedPerShare
            stock_numeric_orgin_data[i, 8] = esp
            stock_numeric_orgin_data[i, 9] = bvps
            stock_numeric_orgin_data[i, 10] = pb
            stock_numeric_orgin_data[i, 11] = undp
            stock_numeric_orgin_data[i, 12] = perundp
            stock_numeric_orgin_data[i, 13] = rev
            stock_numeric_orgin_data[i, 14] = profit
            stock_numeric_orgin_data[i, 15] = gpr
            stock_numeric_orgin_data[i, 16] = npr
            stock_numeric_orgin_data[i, 17] = holders

            i = i + 1

        stock_numeric_data = stock_numeric_orgin_data.T

        # 以下是离群点分析，使用dbscan算法
        mean_matrix = np.mean(stock_numeric_data, axis = 0)
        zeromean_matrix = stock_numeric_data - mean_matrix
        matrix_min, matrix_max = zeromean_matrix.min(), zeromean_matrix.max()
        normaliz_matrix = (zeromean_matrix - matrix_min) / (matrix_max - matrix_min)

        dbscan_min_dist = 100
        dbscan_min_samples = 100
        m, n = np.shape(normaliz_matrix.T)
        xMax = np.max(normaliz_matrix.T, 0)
        xMin = np.min(normaliz_matrix.T, 0)
        dbscan_eps = ((np.prod(xMax - xMin) * dbscan_min_dist * math.gamma(0.5 * n + 1)) / (m * math.sqrt(math.pi ** n))) ** (1.0 / n)

        print("eps：%f, min_samples:%d" %(dbscan_eps, dbscan_min_samples))
        estimator = DBSCAN(eps=dbscan_eps, min_samples=dbscan_min_samples)

        estimator.fit(normaliz_matrix.T)
        label_pred = estimator.labels_

        # 打印离群点的股票信息
        print("利用dbscan分析的离群点为：")
        for i in np.ndarray.tolist(stock_index_data[label_pred == -1]):
            print(stock_info[i])

        # 剔除离群点后计算皮尔森参数做相关分析
        stock_numeric_data = (stock_numeric_data.T[label_pred == 0]).T
        pearson_correlation_coefficient = np.corrcoef(stock_numeric_data)
        fig, ax = plt.subplots(figsize=(18, 18))
        cmap = sns.cubehelix_palette(start=1, rot=3, gamma=0.8, as_cmap=True)
        sns.heatmap(np.round(pearson_correlation_coefficient, 2), cmap = cmap, annot=True, vmax=1, vmin=-1, linewidths=0.05, fmt='.1g', ax = ax)
        ax.set_title('各个属性间的皮尔森相关系数，用于检验多重共线性', fontsize=18, fontproperties=font_set)
        plt.show()


        stock_numeric_data_reduce_result = PCA.PCA.pca_by_dim(stock_numeric_data, 3)
        for_draw_matrix = stock_numeric_data_reduce_result[0]

        x = np.ndarray.tolist(for_draw_matrix[0])
        x = x[0]

        y = np.ndarray.tolist(for_draw_matrix[1])
        y = y[0]

        z= np.ndarray.tolist(for_draw_matrix[2])
        z = z[0]

        # 降到3维绘图看信息
        ax = plt.subplot(111, projection='3d')  # 创建一个三维的绘图工程
        ax.set_title('降到3维之后的分布', fontsize=18, fontproperties=font_set)
        ax.set_zlabel('Z')
        ax.set_ylabel('Y')
        ax.set_xlabel('X')

        plt.scatter(x, y, z)
        plt.show()

        # 降到2维绘图看信息
        fig, ax = plt.subplots(figsize=(18, 18))
        ax.set_title('降到2维之后的分布', fontsize=18, fontproperties=font_set)
        plt.scatter(x, y, marker='x', color='red', s=40, label='点')
        ax.set_ylabel('Y')
        ax.set_xlabel('X')

        plt.scatter(x, y)
        plt.show()

        # 降到1维绘图看信息
        fig, ax = plt.subplots(figsize=(18, 18))
        ax.set_title('降到1维之后的分布', fontsize=18, fontproperties=font_set)
        y = np.zeros(len(x))
        plt.scatter(x, y, marker='x', color='red', s=40, label='点')
        ax.set_ylabel('Y')
        ax.set_xlabel('X')

        plt.scatter(x, y)
        plt.show()


        msg = '已完成股票信息无监督聚类'
        PyQt5GUI.PyQt5GUI.only_instance.log_msg(msg)