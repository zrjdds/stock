#coding=utf-8

from Data import StockDataOperator
from Data import StockDataManager
from Analyze import BasicAnalyze

import datetime
import numpy as np
from GUI import PyQt5GUI

class LiuAnalyze:
    def __init__(self):
        pass

    @staticmethod
    def liu_stock_bottom(days=180, offset=10, ratio=3):
        start_analyze_time = datetime.datetime.now()

        stock_code_list = StockDataManager.StockDataManager.load_all_stock_code()

        time_temp1 = datetime.datetime.now() - datetime.timedelta(days=days)
        start_datetime = time_temp1.strftime('%Y-%m-%d')

        time_temp2 = datetime.datetime.now()
        end_datetime = time_temp2.strftime('%Y-%m-%d')

        result = []

        for stock_code in stock_code_list:
            stock_data = StockDataManager.StockDataManager.load_stock_data_by_stock_code(stock_code, 'all', start_datetime, end_datetime, 'DESC')

            print('刘见底股票，正在分析 %s' %stock_code)
            item = {}

            if stock_data is not None:
                stock_close_list = []
                stock_date_list = []

                stock_data_len = len(stock_data)
                i = 0
                while i < stock_data_len:
                    stock_close_list.append(stock_data[i][2])
                    stock_date_list.append(stock_data[i][1])
                    i = i + 1

                try:
                    i = 0
                    while i < stock_data_len - 1:
                        if stock_close_list[i] < stock_close_list[i+1]:
                            i = i + 1
                        elif stock_close_list[i] == stock_close_list[i+1]:
                            i = i + 1
                        else:
                            if stock_close_list[i] - stock_close_list[i+1] < stock_close_list[i+1] / offset:
                                i = i + 1
                            else:
                                break

                    if i > 0:
                        if stock_close_list[i-1] > ratio*stock_close_list[0]:
                            item['stock_code'] = stock_code
                            item['days'] = i
                            item['analyze_days'] = stock_data_len
                            item['offset'] = offset
                            item['ratio'] = ratio
                            result.append(item)

                except Exception as err:
                    print(err)
                    continue

        StockDataManager.StockDataManager.write_liu_analyze_stock_bottom(result)
        PyQt5GUI.PyQt5GUI.only_instance.liu_stock_bottom_run_flag = False
        PyQt5GUI.PyQt5GUI.only_instance.log_msg("已完成刘见底股票分析")

        end_analyze_time = datetime.datetime.now()

        cost_minutes = (end_analyze_time - start_analyze_time).seconds / 60

        print('本次分析共花费 %f 分钟' %cost_minutes)


        return result

    @staticmethod
    def liu_stock_trend(days=180):
        stock_code_list = StockDataManager.StockDataManager.load_all_stock_code()

        time_temp1 = datetime.datetime.now() - datetime.timedelta(days=days)
        start_datetime = time_temp1.strftime('%Y-%m-%d')

        time_temp2 = datetime.datetime.now()
        end_datetime = time_temp2.strftime('%Y-%m-%d')

        result = []

        for stock_code in stock_code_list:
            stock_data = StockDataManager.StockDataManager.load_stock_data_by_stock_code(stock_code, 'all', start_datetime, end_datetime, 'ASC')

            item = {}

            if stock_data is not None:
                stock_close_list = []

                stock_data_len = len(stock_data)
                i = 0
                while i < stock_data_len:
                    stock_close_list.append(stock_data[i][2])
                    i = i + 1

                try:
                    trend = BasicAnalyze.BasicAnalyze.trend_judge(stock_close_list)
                except Exception:
                    trend = "无法分析"

                item['stock_code'] = stock_code
                item['stock_trend'] = trend
                item['analyze_days'] = stock_data_len
                result.append(item)
            else:
                item['stock_code'] = stock_code
                item['stock_trend'] = '没有数据'
                item['analyze_days'] = stock_data_len
                result.append(item)

        StockDataManager.StockDataManager.write_liu_analyze_stock_trend(result)
        PyQt5GUI.PyQt5GUI.only_instance.liu_stock_trend_month_run_flag = False
        PyQt5GUI.PyQt5GUI.only_instance.log_msg("已完成刘股票趋势分析")

        return result
