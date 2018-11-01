#coding=utf-8

from Data import StockDataOperator
import datetime


if __name__ == '__main__':

    # 取所有代码
    # sdo = StockDataOperator.StockDataOperator()
    # sdo.init_db_info()
    # stock_code_list = sdo.fetch_all_stock_code()
    # for stock_code in stock_code_list:
    #     sdo.append_stock_code(stock_code)

    # sdo.fetch_history_data(start_dt='20180913', end_dt='20370101')

    sdo = StockDataOperator.StockDataOperator()
    sdo.init_db_info()
    stock_code_list = sdo.fetch_all_stock_code()
    for stock_code in stock_code_list:
         sdo.append_stock_code(stock_code)

    #sdo.fetch_history_data(start_dt='20010101', end_dt='20370101', stock_code='601068.SH')

    sdo = StockDataOperator.StockDataOperator()
    sdo.init_db_info()
    sdo.fetch_history_data_from_baostock('20160101', '20181010', '601857.SH')