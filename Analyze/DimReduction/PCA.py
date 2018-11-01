#coding=utf-8
from numpy import *

class PCA:
    '''通过方差的百分比来计算将数据降到多少维是比较合适的，函数传入的参数是特征值和百分比percentage，返回需要降到的维度数num'''
    @staticmethod
    def eig_val_pct(eig_vals, percentage):
        # 使用numpy中的sort()对特征值按照从小到大排序
        sortArray=sort(eig_vals)

        # 特征值从大到小排序
        sortArray=sortArray[-1::-1]

        # 数据全部的方差arraySum
        arraySum = sum(sortArray)

        tempSum=0
        num=0
        for i in sortArray:
            tempSum += i
            num += 1
            if tempSum >= arraySum*percentage:
                return num

        return num

    @staticmethod
    def pca_by_dim(high_dim_data_matrix, dim = 2):

        # 对每一列求平均值，因为协方差的计算中需要减去均值
        mean_matrix = mean(high_dim_data_matrix, axis = 0)

        # 0均值处理
        zeromean_matrix = high_dim_data_matrix - mean_matrix

        # 求最大最小值
        matrix_min, matrix_max = zeromean_matrix.min(), zeromean_matrix.max()
        # (矩阵元素-最小值)/(最大值-最小值),得到标准化的数据(归一)
        normaliz_matrix = (zeromean_matrix - matrix_min) / (matrix_max - matrix_min)

        # 协方差矩阵
        cov_matrix = cov(normaliz_matrix, rowvar = 1)

        # 利用numpy中寻找特征值和特征向量的模块linalg中的eig()方法
        # mat函数是将对象转换为matrix类型
        eig_vals, eig_vects = linalg.eig(mat(cov_matrix))

        k = dim

        # 对特征值eig_vals从小到大排序
        eig_val_ind = argsort(eig_vals)

        # 从排好序的特征值，从后往前取k个，这样就实现了特征值的从大到小排列
        eig_val_ind = eig_val_ind[:-(k+1):-1]

        # 返回排序后特征值对应的特征向量red_eig_vects（主成分）
        red_eig_vects = eig_vects[:,eig_val_ind]

        # 将原始数据投影到主成分上得到新的低维数据low_dim_data_matrix
        low_dim_data_matrix = red_eig_vects.T * normaliz_matrix

        return low_dim_data_matrix, eig_vals, eig_vects,eig_val_ind,k,red_eig_vects.T


    '''pca函数有两个参数，其中high_dim_data_matrix是已经转换成矩阵matrix形式的数据集，列表示特征；其中的percentage表示取前多少个特征需要达到的方差占比，默认为0.9'''
    @staticmethod
    def pca_by_percentage(high_dim_data_matrix, percentage = 0.9):

        # 对每一列求平均值，因为协方差的计算中需要减去均值
        mean_matrix = mean(high_dim_data_matrix, axis = 0)

        # 0均值处理
        zeromean_matrix = high_dim_data_matrix - mean_matrix

        # 求最大最小值
        matrix_min, matrix_max = zeromean_matrix.min(), zeromean_matrix.max()
        # (矩阵元素-最小值)/(最大值-最小值),得到标准化的数据(归一)
        normaliz_matrix = (zeromean_matrix - matrix_min) / (matrix_max - matrix_min)

        # 协方差矩阵
        cov_matrix = cov(normaliz_matrix, rowvar = 1)

        # 利用numpy中寻找特征值和特征向量的模块linalg中的eig()方法
        # mat函数是将对象转换为matrix类型
        eig_vals, eig_vects = linalg.eig(mat(cov_matrix))

        # 要达到方差的百分比percentage，需要前k个向量
        k = PCA.eig_val_pct(eig_vals, percentage)


        # 对特征值eig_vals从小到大排序
        eig_val_ind = argsort(eig_vals)

        # 从排好序的特征值，从后往前取k个，这样就实现了特征值的从大到小排列
        eig_val_ind = eig_val_ind[:-(k+1):-1]

        # 返回排序后特征值对应的特征向量red_eig_vects（主成分）
        red_eig_vects = eig_vects[:,eig_val_ind]

        # 将原始数据投影到主成分上得到新的低维数据low_dim_data_matrix
        low_dim_data_matrix = red_eig_vects.T * normaliz_matrix

        return low_dim_data_matrix, eig_vals, eig_vects,eig_val_ind,k,red_eig_vects.T

