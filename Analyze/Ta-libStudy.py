#coding=utf-8

from talib import CDL2CROWS
import numpy as np

open = np.array([ 8.34, 8.43, 8.38, 8.38, 8.33, 8.36, 8.53, 8.34, 8.3,  8.42, 8.52, 8.67, 9.22, 9.21, 8.96])
close = np.array([ 8.43, 8.36, 8.4,  8.34, 8.34, 8.46, 8.41, 8.28, 8.4,  8.51, 8.62, 9.11, 9.18, 8.96, 8.94])
high = np.array([ 8.55, 8.44, 8.42, 8.39, 8.42, 8.54, 8.55, 8.37, 8.42, 8.57, 8.72, 9.38, 9.3,  9.24, 9.05])
low = np.array([ 8.33, 8.31, 8.34, 8.32, 8.31, 8.36, 8.38, 8.24, 8.3,  8.38, 8.43, 8.64, 9.07, 8.91, 8.81])

print(CDL2CROWS(open, high, low, close))