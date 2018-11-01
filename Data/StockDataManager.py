#coding=utf-8
from Data import StockDataOperator
from GUI import PyQt5GUI

class StockDataManager:

    def __init__(self):
        pass

    @staticmethod
    def null_op():
        pass

    @staticmethod
    def write_liu_analyze_stock_trend(stock_trend):
        sdo = StockDataOperator.StockDataOperator()
        sdo.init_db_info()
        sdo.write_liu_analyze_stock_trend(stock_trend)

    @staticmethod
    def write_liu_analyze_stock_bottom(stock_bottom):
        sdo = StockDataOperator.StockDataOperator()
        sdo.init_db_info()
        sdo.write_liu_analyze_stock_bottom(stock_bottom)

    @staticmethod
    def load_liu_analyze_stock_trend():
        sdo = StockDataOperator.StockDataOperator()
        sdo.init_db_info()
        return sdo.load_liu_analyze_stock_trend()

    @staticmethod
    def load_liu_analyze_stock_bottom():
        sdo = StockDataOperator.StockDataOperator()
        sdo.init_db_info()
        return sdo.load_liu_analyze_stock_bottom()

    @staticmethod
    def load_stock_info():
        sdo = StockDataOperator.StockDataOperator()
        sdo.init_db_info()
        return sdo.load_stock_info()

    @staticmethod
    def load_all_stock_code():
        sdo = StockDataOperator.StockDataOperator()
        sdo.init_db_info()
        return sdo.load_all_stock_code()

    @staticmethod
    def load_stock_data_by_stock_code(stock_code, require_type='all', start_dt='2001-01-01', end_dt='2037-01-01', order_by='ASC'):
        sdo = StockDataOperator.StockDataOperator()
        sdo.init_db_info()
        return sdo.load_stock_data(stock_code, require_type, start_dt, end_dt, order_by)

    @staticmethod
    def fetch_all_stock_data():
        sdo = StockDataOperator.StockDataOperator()
        sdo.init_db_info()
        stock_code_list = sdo.fetch_all_stock_code()
        for stock_code in stock_code_list:
            sdo.append_stock_code(stock_code)

        sdo.fetch_history_data(start_dt='2001-01-01', end_dt='2037-01-01')

        PyQt5GUI.PyQt5GUI.only_instance.fetch_lastweek_stock_data_flag = False
        PyQt5GUI.PyQt5GUI.only_instance.log_msg("已完成所有股票数据抓取")

    @staticmethod
    def fetch_lastweek_stock_data():
        sdo = StockDataOperator.StockDataOperator()
        sdo.init_db_info()
        stock_code_list = sdo.fetch_all_stock_code()
        for stock_code in stock_code_list:
            sdo.append_stock_code(stock_code)

        sdo.fetch_lastweek_data()

        PyQt5GUI.PyQt5GUI.only_instance.fetch_lastweek_stock_data_flag = False
        PyQt5GUI.PyQt5GUI.only_instance.log_msg("已完成7天股票数据抓取")

    @staticmethod
    def fetch_yesterday_stock_data():
        sdo = StockDataOperator.StockDataOperator()
        sdo.init_db_info()
        stock_code_list = sdo.fetch_all_stock_code()
        for stock_code in stock_code_list:
            sdo.append_stock_code(stock_code)

        sdo.fetch_yesterday_data()
        PyQt5GUI.PyQt5GUI.only_instance.fetch_yesterday_stock_data_flag = False
        PyQt5GUI.PyQt5GUI.only_instance.log_msg("已完成昨天股票数据抓取")

    @staticmethod
    def fetch_stock_info():
        sdo = StockDataOperator.StockDataOperator()
        sdo.init_db_info()
        sdo.fetch_stock_info()

        PyQt5GUI.PyQt5GUI.only_instance.fetch_stock_info_flag = False
        PyQt5GUI.PyQt5GUI.only_instance.log_msg("已完成股票信息抓取")