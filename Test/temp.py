import numpy as np
import pandas as pd
from numpy import *

high_dim_data_matrix = np.zeros([3, 2])
high_dim_data_matrix[0, 0] = 1
high_dim_data_matrix[0, 1] = 2
high_dim_data_matrix[1, 0] = 3
high_dim_data_matrix[1, 1] = 4
high_dim_data_matrix[2, 0] = 5
high_dim_data_matrix[2, 1] = 6

mean_matrix = mean(high_dim_data_matrix, axis = 0)
zeromean_matrix = high_dim_data_matrix - mean_matrix

cov_matrix = cov(zeromean_matrix, rowvar=1)

#print(cov_matrix)


a = np.array([1,2,3])
b = np.array([2,5,8])
x = np.vstack((a,b))
#print(x)
#print(np.corrcoef(a, b))
#print(np.corrcoef(x))


a = pd.Series([1,2,3,4,5,6,7,8,9,10])
b = pd.Series([2,4,1,5,1,3,6,2,7,0])
c = pd.Series([0,3,2,1,4,7,1,9,6,2])
x = np.vstack((a,b,c))
print(x)
r = np.corrcoef(x)
print(r)

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

data = np.random.randint(0, 255, size=[40, 40, 40])

x, y, z = data[0], data[1], data[2]
ax = plt.subplot(111, projection='3d')  # 创建一个三维的绘图工程

print(x)
print(y)
print(z)
#  将数据点分成三部分画，在颜色上有区分度
ax.scatter(x[:10], y[:10], z[:10], c='y')  # 绘制数据点
ax.scatter(x[10:20], y[10:20], z[10:20], c='r')
ax.scatter(x[30:40], y[30:40], z[30:40], c='g')

ax.set_zlabel('Z')  # 坐标轴
ax.set_ylabel('Y')
ax.set_xlabel('X')
plt.show()
