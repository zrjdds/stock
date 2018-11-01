#coding=utf-8

import numpy as np
from statsmodels.tsa.stattools import adfuller as ADF


class BasicAnalyze:
    def __init__(self):
        pass

    @staticmethod
    def stage_analyze(input_data, delta):
        data_size = len(input_data)
        density_array = np.zeros(data_size)

        for i in np.arange(data_size):
            density = 0
            density_count = 0

            for j in np.arange(i - delta, i + delta + 1):
                if j >= 0 and j < data_size:
                    density = density + input_data[j]
                    density_count = density_count + 1

            density_array[i] = density / density_count

        return density_array

    @staticmethod
    def trend_judge(input_data):
        # 计算总趋势秩次和
        input_data = np.array(input_data)
        n = input_data.shape[0]
        sum_sgn = 0
        for i in np.arange(n):
            if i <= (n - 1):
                for j in np.arange(i + 1, n):
                    if input_data[j] > input_data[i]:
                        sum_sgn = sum_sgn + 1
                    elif input_data[j] < input_data[i]:
                        sum_sgn = sum_sgn - 1
                    else:
                        sum_sgn = sum_sgn
        # 计算Z统计值
        if n <= 10:
            Z_value = sum_sgn / (n * (n - 1) / 2)
        else:
            if sum_sgn > 0:
                Z_value = (sum_sgn - 1) / np.sqrt(n * (n - 1) * (2 * n + 5) / 18)
            elif sum_sgn == 0:
                Z_value = 0
            else:
                Z_value = (sum_sgn + 1) / np.sqrt(n * (n - 1) * (2 * n + 5) / 18)

        # 时序平稳性检验之ADF检验（数据不易太少）
        ADF_result = ADF(input_data, 0)
        # 趋势描述
        # 99% ——> +—2.576
        # 95% ——> +—1.96
        # 90% ——> +—1.645
        if ADF_result[1] < 0.01:
            result_desc = '呈现稳定趋势'
        else:
            if np.abs(Z_value) > 1.96 and np.abs(Z_value) <= 2.576:
                if Z_value > 0:
                    result_desc = '呈现上升趋势'
            else:
                result_desc = '呈现下降趋势'
            if np.abs(Z_value) > 2.576:
                if Z_value > 0:
                    result_desc = '呈现明显上升趋势'
                else:
                    result_desc = '呈现明显下降趋势'
            else:
                result_desc = '上升/下降趋势不明显'
        return result_desc


if __name__ == '__main__':
     close_price = [10, 12, 13, -2, 16, -4, 8, 10, -3, -100]
     BasicAnalyze.stage_analyze(close_price, 3)
