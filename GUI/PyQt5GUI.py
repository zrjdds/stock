#coding=utf-8


import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtCore import QDate, QTime, QDateTime, Qt

import numpy as np

from Data import StockDataManager
from GUI.StockPainter import StockBasicKlinePainter
from GUI.StockPainter import StockPricePainter
from Analyze import LiuAnalyze
from Analyze import MLAnalyze

import threading
import datetime
from GUI.ParameterDialog import LiuStockBottomParameterDialog
from GUI.ParameterDialog import KLineParameterDialog

class PyQt5GUI(QMainWindow):

    only_instance = None

    def __init__(self):
        super().__init__()

        self.liu_stock_bottom_run_flag = False
        self.liu_stock_trend_run_flag = False
        self.fetch_stock_info_flag = False
        self.fetch_yesterday_stock_data_flag = False
        self.fetch_lastweek_stock_data_flag = False
        self.fetch_all_stock_data_flag = False

        self.layout = QVBoxLayout()
        self.log_msg_widget = QListWidget()
        self.last_main_widget = None
        self.layout_widget = QWidget()

        self.init_UI()
        self.log_msg('初始化完成')

        PyQt5GUI.only_instance = self

    def init_UI(self):
        self.init_menu()
        self.setWindowTitle("股票分析")
        self.setGeometry(0, 0, 1500, 1000)


        self.layout_widget.setLayout(self.layout)
        self.setCentralWidget(self.layout_widget)

        self.report_stock_info()

    def init_menu(self):
        menu_bar = self.menuBar()

        data_menu = menu_bar.addMenu('数据')
        fetch_stock_info_action = QAction('抓取实时股票列表', self)
        fetch_stock_info_action.triggered.connect(self.data_fetch_stock_info)
        data_menu.addAction(fetch_stock_info_action)
        fetch_stock_data_menu = QMenu('抓取实时股票数据', self)
        fetch_all_stock_data_action = QAction('抓取所有实时股票数据', self)
        fetch_all_stock_data_action.triggered.connect(self.data_fetch_all_stock_data)
        fetch_lastweek_stock_data_action = QAction('抓取7天内实时股票数据', self)
        fetch_lastweek_stock_data_action.triggered.connect(self.data_fetch_lastweek_stock_data)
        fetch_yesterday_stock_data_action = QAction('抓取昨天实时股票数据', self)
        fetch_yesterday_stock_data_action.triggered.connect(self.data_fetch_yesterday_stock_data)
        fetch_stock_data_menu.addAction(fetch_all_stock_data_action)
        fetch_stock_data_menu.addAction(fetch_lastweek_stock_data_action)
        fetch_stock_data_menu.addAction(fetch_yesterday_stock_data_action)
        data_menu.addMenu(fetch_stock_data_menu)
        clear_analyze_data_menu = QMenu('清除数据', self)
        clear_analyze_liu_stock_trend_action = QAction('清除刘股票趋势分析数据', self)
        clear_analyze_data_menu.addAction(clear_analyze_liu_stock_trend_action)
        data_menu.addMenu(clear_analyze_data_menu)

        analyze_menu = menu_bar.addMenu('分析')
        liu_analyze_menu = QMenu('刘分析', self)
        liu_analyze_stock_trend_action = QAction('股票趋势分析', self)
        liu_analyze_menu.addAction(liu_analyze_stock_trend_action)
        liu_analyze_stock_trend_action.triggered.connect(self.analyze_liu_stock_trend)

        liu_analyze_stock_bottom_action = QAction('见底股票分析', self)
        liu_analyze_menu.addAction(liu_analyze_stock_bottom_action)
        liu_analyze_stock_bottom_action.triggered.connect(self.analyze_liu_stock_bottom)

        analyze_menu.addMenu(liu_analyze_menu)

        ml_analyze_menu = QMenu('机器学习分析', self)
        ml_analyze_lstm_close_forcast_action = QAction('LSTM收盘价预测', self)
        ml_analyze_menu.addAction(ml_analyze_lstm_close_forcast_action)
        ml_analyze_lstm_close_forcast_action.triggered.connect(self.analyze_ml_lstm_close_forcast)

        ml_analyze_stock_info_clustering_action = QAction('股票信息无监督聚类', self)
        ml_analyze_menu.addAction(ml_analyze_stock_info_clustering_action)
        ml_analyze_stock_info_clustering_action.triggered.connect(self.analyze_ml_stock_info_clustering)

        analyze_menu.addMenu(ml_analyze_menu)

        draw_menu = menu_bar.addMenu('图形')
        draw_stock_kline_action = QAction('股票K线图', self)
        draw_stock_kline_action.triggered.connect(self.draw_stock_kline)
        draw_menu.addAction(draw_stock_kline_action)

        report_menu = menu_bar.addMenu('报表')

        report_stock_info_action = QAction('股票信息表', self)
        report_stock_info_action.triggered.connect(self.report_stock_info)
        report_menu.addAction(report_stock_info_action)

        liu_report_menu = QMenu('刘报表', self)
        liu_report_stock_trend_action = QAction('股票趋势分析结果', self)
        liu_report_menu.addAction(liu_report_stock_trend_action)
        liu_report_stock_trend_action.triggered.connect(self.report_liu_stock_trend)

        liu_report_stock_bottom_action = QAction('见底股票分析结果', self)
        liu_report_menu.addAction(liu_report_stock_bottom_action)
        liu_report_stock_bottom_action.triggered.connect(self.report_liu_stock_bottom)

        report_menu.addMenu(liu_report_menu)

        ml_report_menu = QMenu('机器学习报表', self)
        ml_report_lstm_close_forcast_action = QAction('LSTM收盘价预测结果', self)
        ml_report_menu.addAction(ml_report_lstm_close_forcast_action)
        ml_report_menu.triggered.connect(self.report_ml_lstm_close_forcast)

        report_menu.addMenu(ml_report_menu)

        about_menu = menu_bar.addMenu('关于')

    def data_fetch_stock_info(self):
        if self.fetch_stock_info_flag == True:
            QMessageBox.information(self, "敬告", "正在进行中，请稍等", QMessageBox.Yes)
        else:
            self.fetch_stock_info_flag = True
            t = threading.Thread(target=StockDataManager.StockDataManager.fetch_stock_info)
            t.setDaemon(True)
            t.start()
            self.log_msg("开始执行抓取股票信息")

    def data_fetch_lastweek_stock_data(self):
        if self.fetch_lastweek_stock_data_flag == True:
            QMessageBox.information(self, "敬告", "正在进行中，请稍等", QMessageBox.Yes)
        else:
            self.fetch_lastweek_stock_data_flag = True
            t = threading.Thread(target=StockDataManager.StockDataManager.fetch_lastweek_stock_data)
            t.setDaemon(True)
            t.start()
            self.log_msg("开始执行抓取7天内股票数据")

    def data_fetch_yesterday_stock_data(self):
        if self.fetch_yesterday_stock_data_flag == True:
            QMessageBox.information(self, "敬告", "正在进行中，请稍等", QMessageBox.Yes)
        else:
            self.fetch_yesterday_stock_data_flag = True
            t = threading.Thread(target=StockDataManager.StockDataManager.fetch_lastweek_stock_data)
            t.setDaemon(True)
            t.start()
            self.log_msg("开始执行抓取昨天股票数据")

    def data_fetch_all_stock_data(self):
        if self.fetch_all_stock_data_flag == True:
            QMessageBox.information(self, "敬告", "正在进行中，请稍等", QMessageBox.Yes)
        else:
            self.fetch_all_stock_data_flag = True
            t = threading.Thread(target=StockDataManager.StockDataManager.fetch_all_stock_data)
            t.setDaemon(True)
            t.start()
            self.log_msg("开始执行抓取所有股票数据")

    def draw_stock_kline(self):
        dialog = KLineParameterDialog.KLineParameterDialog()
        if dialog.exec_():
            try:
                stock_code = dialog.stock_code.text()
                start_dt = dialog.start_calendar.selectedDate().toString(Qt.ISODate)
                end_dt = dialog.end_calendar.selectedDate().toString(Qt.ISODate)

                # start_dt = start_iso_date[0:4] + start_iso_date[5:7] + start_iso_date[8:10]
                # end_dt = end_iso_date[0:4] + end_iso_date[5:7] + end_iso_date[8:10]

                hist_data = StockDataManager.StockDataManager.load_stock_data_by_stock_code(stock_code, 'all', start_dt, end_dt, 'ASC')

                if hist_data is None:
                    QMessageBox.information(self, "敬告", "没有数据或者数据异常", QMessageBox.Yes)
                    return

                win = StockBasicKlinePainter.StockBasicKlinePainter.produce_basic_kline_windows(hist_data, stock_code)
                msg = '完成代码为 %s 的股票K线绘制' % stock_code
                self.log_msg(msg)
                self.subwin = win
                win.show()

            except Exception as err:
                print(err)


    def report_stock_info(self):
        stock_info = StockDataManager.StockDataManager.load_stock_info()

        if stock_info is None:
            return

        stock_count = len(stock_info)
        stock_info_table_widget = QTableWidget(stock_count, 23)
        stock_info_table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        stock_info_table_widget.setSelectionBehavior(QTableWidget.SelectRows)
        stock_info_table_widget.setSelectionMode(QTableWidget.SingleSelection)
        stock_info_table_widget.setAlternatingRowColors(True)
        #stock_info_table_widget.setSortingEnabled(True)
        stock_info_table_widget.horizontalHeader().setStretchLastSection(True)
        stock_info_table_widget.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        stock_info_table_widget.setHorizontalHeaderLabels(
            [
                '代码',
                '名称',
                '所属行业',
                '地区',
                '市盈率',
                '流通股本(亿)',
                '总股本(亿)',
                '总资产(万)',
                '流动资产',
                '固定资产',
                '公积金',
                '每股公积金',
                '每股收益',
                '每股净资',
                '市净率',
                '上市日期',
                '未分利润',
                '每股未分配',
                '收入同比(%)',
                '利润同比(%)',
                '毛利率(%)',
                '净利润率(%)',
                '股东人数'
            ])

        if stock_info is None:
            QMessageBox.information(self, "敬告", "暂时没有数据", QMessageBox.Yes)
            return

        i = 0
        for stock in stock_info:
            stock_code_item = QTableWidgetItem(stock[0])
            name_item = QTableWidgetItem(stock[1])
            industry_item = QTableWidgetItem(stock[2])
            area_item = QTableWidgetItem(stock[3])
            pe_item = QTableWidgetItem(repr(stock[4]))
            outstanding_item = QTableWidgetItem(repr(stock[5]))
            totals_item = QTableWidgetItem(repr(stock[6]))
            totalAssets_item = QTableWidgetItem(repr(stock[7]))
            liquidAssets_item = QTableWidgetItem(repr(stock[8]))
            fixedAssets_item = QTableWidgetItem(repr(stock[9]))
            reserved_item = QTableWidgetItem(repr(stock[10]))
            reservedPerShare_item = QTableWidgetItem(repr(stock[11]))
            esp_item = QTableWidgetItem(repr(stock[12]))
            bvps_item = QTableWidgetItem(repr(stock[13]))
            pb_item = QTableWidgetItem(repr(stock[14]))
            timeToMarket_item = QTableWidgetItem(repr(stock[15]))
            undp_item = QTableWidgetItem(repr(stock[16]))
            perundp_item = QTableWidgetItem(repr(stock[17]))
            rev_item = QTableWidgetItem(repr(stock[18]))
            profit_item = QTableWidgetItem(repr(stock[19]))
            gpr_item = QTableWidgetItem(repr(stock[20]))
            npr_item = QTableWidgetItem(repr(stock[21]))
            holders_item = QTableWidgetItem(repr(stock[22]))

            stock_info_table_widget.setItem(i, 0, stock_code_item)
            stock_info_table_widget.setItem(i, 1, name_item)
            stock_info_table_widget.setItem(i, 2, industry_item)
            stock_info_table_widget.setItem(i, 3, area_item)
            stock_info_table_widget.setItem(i, 4, pe_item)
            stock_info_table_widget.setItem(i, 5, outstanding_item)
            stock_info_table_widget.setItem(i, 6, totals_item)
            stock_info_table_widget.setItem(i, 7, totalAssets_item)
            stock_info_table_widget.setItem(i, 8, liquidAssets_item)
            stock_info_table_widget.setItem(i, 9, fixedAssets_item)
            stock_info_table_widget.setItem(i, 10, reserved_item)
            stock_info_table_widget.setItem(i, 11, reservedPerShare_item)
            stock_info_table_widget.setItem(i, 12, esp_item)
            stock_info_table_widget.setItem(i, 13, bvps_item)
            stock_info_table_widget.setItem(i, 14, pb_item)
            stock_info_table_widget.setItem(i, 15, timeToMarket_item)
            stock_info_table_widget.setItem(i, 16, undp_item)
            stock_info_table_widget.setItem(i, 17, perundp_item)
            stock_info_table_widget.setItem(i, 18, rev_item)
            stock_info_table_widget.setItem(i, 19, profit_item)
            stock_info_table_widget.setItem(i, 20, gpr_item)
            stock_info_table_widget.setItem(i, 21, npr_item)
            stock_info_table_widget.setItem(i, 22, holders_item)

            i = i + 1

        #self.setCentralWidget(stock_info_table_widget)

        self.set_main_widget(stock_info_table_widget)

        stock_info_table_widget.itemDoubleClicked.connect(self.on_stock_code_widget_item_doubleclicked)




    def report_liu_stock_bottom(self):
        if self.liu_stock_bottom_run_flag == True:
            reply = QMessageBox.question(self, '敬告', '有新的分析在执行，是否查看旧的结果?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.No:
                return

        result = StockDataManager.StockDataManager.load_liu_analyze_stock_bottom()
        if result is None:
            QMessageBox.information(self, "敬告", "暂时没有数据", QMessageBox.Yes)
            return

        result_count = len(result)
        if result_count == 0:
            QMessageBox.information(self, "敬告", "暂时没有数据", QMessageBox.Yes)
            return

        stock_bottom_table_widget = QTableWidget(result_count, 5)
        stock_bottom_table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        stock_bottom_table_widget.setSelectionBehavior(QTableWidget.SelectRows)
        stock_bottom_table_widget.setSelectionMode(QTableWidget.SingleSelection)
        stock_bottom_table_widget.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        stock_bottom_table_widget.horizontalHeader().setStretchLastSection(True)
        stock_bottom_table_widget.setAlternatingRowColors(True)
        stock_bottom_table_widget.setHorizontalHeaderLabels(
            [
                '股票代码',
                '总体趋势向下天数',
                '分析所用的数据天数',
                '最大允许波动价格比例',
                '最小下跌倍数'
            ])

        i = 0
        for stock in result:
            new_item = QTableWidgetItem(stock[0])
            stock_bottom_table_widget.setItem(i, 0, new_item)
            new_item = QTableWidgetItem(repr(stock[1]))
            stock_bottom_table_widget.setItem(i, 1, new_item)
            new_item = QTableWidgetItem(repr(stock[2]))
            stock_bottom_table_widget.setItem(i, 2, new_item)
            new_item = QTableWidgetItem(repr(stock[3]))
            stock_bottom_table_widget.setItem(i, 3, new_item)
            new_item = QTableWidgetItem(repr(stock[4]))
            stock_bottom_table_widget.setItem(i, 4, new_item)
            i = i + 1

        self.set_main_widget(stock_bottom_table_widget)
        stock_bottom_table_widget.itemDoubleClicked.connect(self.on_stock_code_widget_item_doubleclicked)

    def report_liu_stock_trend(self):
        if self.liu_stock_trend_run_flag == True:
            reply = QMessageBox.question(self, '敬告', '有新的分析在执行，是否查看旧的结果?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.No:
                return

        result = StockDataManager.StockDataManager.load_liu_analyze_stock_trend()
        if result is None:
            QMessageBox.information(self, "敬告", "暂时没有数据", QMessageBox.Yes)
            return

        result_count = len(result)
        if result_count == 0:
            QMessageBox.information(self, "敬告", "暂时没有数据", QMessageBox.Yes)
            return

        stock_trend_table_widget = QTableWidget(result_count, 3)
        stock_trend_table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        stock_trend_table_widget.setSelectionBehavior(QTableWidget.SelectRows)
        stock_trend_table_widget.setSelectionMode(QTableWidget.SingleSelection)
        stock_trend_table_widget.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        stock_trend_table_widget.horizontalHeader().setStretchLastSection(True)
        stock_trend_table_widget.setAlternatingRowColors(True)
        stock_trend_table_widget.setHorizontalHeaderLabels(
            [
                '股票代码',
                '趋势',
                '分析所用的数据天数'
            ])

        i = 0
        for stock in result:
            new_item = QTableWidgetItem(stock[0])
            stock_trend_table_widget.setItem(i, 0, new_item)
            new_item = QTableWidgetItem(stock[1])
            stock_trend_table_widget.setItem(i, 1, new_item)
            new_item = QTableWidgetItem(repr(stock[2]))
            stock_trend_table_widget.setItem(i, 2, new_item)
            i = i + 1

        self.set_main_widget(stock_trend_table_widget)
        stock_trend_table_widget.itemDoubleClicked.connect(self.on_stock_code_widget_item_doubleclicked)

    def report_ml_lstm_close_forcast(self):
        stock_code_dialog = QInputDialog()
        stock_code_dialog.setInputMode(0)
        stock_code_dialog.setLabelText("股票代码")
        stock_code_dialog.setWindowTitle("请输入股票代码")
        stock_code_dialog.setOkButtonText(u"确定")
        stock_code_dialog.setCancelButtonText(u"取消")

        if stock_code_dialog.exec_():
            stock_code = stock_code_dialog.textValue()

            try:
                hist_data = StockDataManager.StockDataManager.load_stock_data_by_stock_code(stock_code)

                if hist_data is None:
                    QMessageBox.information(self, "敬告", "没有数据或者数据异常", QMessageBox.Yes)
                    return

                win = StockPricePainter.StockPricePainter.produce_basic_price_windows(hist_data, stock_code)

                self.subwin = win
                win.show()

                msg = '完成代码为 %s 的股票LSTM股票收盘价预测结果绘图' % stock_code
                self.log_msg(msg)
            except Exception as err:
                print(err)
                msg = '代码为 %s 的股票LSTM股票收盘价预测结果绘图' % stock_code
                self.log_msg(msg)




    def on_stock_code_widget_item_doubleclicked(self, item):
        stock_code = item.text()

        try:
            hist_data = StockDataManager.StockDataManager.load_stock_data_by_stock_code(stock_code)

            if hist_data is None:
                QMessageBox.information(self, "敬告", "没有数据或者数据异常", QMessageBox.Yes)
                return

            win = StockBasicKlinePainter.StockBasicKlinePainter.produce_basic_kline_windows(hist_data, stock_code)
            msg = '完成代码为 %s 的股票K线绘制' % stock_code
            self.log_msg(msg)
            self.subwin = win
            win.show()
        except Exception as err:
            print(err)

    def analyze_liu_stock_bottom(self):
        if self.liu_stock_bottom_run_flag == True:
            QMessageBox.information(self, "敬告", "分析正在进行，请等待", QMessageBox.Yes)
        else:
            self.liu_stock_bottom_run_flag = True

            dialog = LiuStockBottomParameterDialog.LiuStockBottomParameterDialog()
            if dialog.exec_():
                try:
                    days = int(dialog.days.text())
                    offset = int(dialog.offset.text())
                    ratio = int(dialog.ratio.text())

                    t = threading.Thread(target=LiuAnalyze.LiuAnalyze.liu_stock_bottom, args=(days,offset,ratio))
                    t.setDaemon(True)
                    t.start()
                    self.log_msg("开始执行刘见底股票分析")

                except Exception as err:
                    print(err)

            # days_dialog = QInputDialog()
            # days_dialog.setInputMode(1)
            # days_dialog.setIntMinimum(60)
            # days_dialog.setIntMaximum(100000)
            # days_dialog.setIntStep(2)
            # days_dialog.setIntValue(60)
            # days_dialog.setLabelText("天数")
            # days_dialog.setWindowTitle("请输入要分析的天数")
            # days_dialog.setOkButtonText(u"确定")
            # days_dialog.setCancelButtonText(u"取消")
                # if days_dialog.exec_():
                # days = days_dialog.intValue()
                # t = threading.Thread(target=LiuAnalyze.LiuAnalyze.liu_stock_bottom, args=(days,))
                # t.setDaemon(True)
                # t.start()
                # self.log_msg("开始执行刘见底股票分析")



    def analyze_liu_stock_trend(self):
        if self.liu_stock_trend_run_flag == True:
            QMessageBox.information(self, "敬告", "分析正在进行，请等待", QMessageBox.Yes)
        else:
            self.liu_stock_trend_run_flag = True

            days_dialog = QInputDialog()
            days_dialog.setInputMode(1)
            days_dialog.setIntMinimum(60)
            days_dialog.setIntMaximum(100000)
            days_dialog.setIntStep(2)
            days_dialog.setIntValue(60)
            days_dialog.setLabelText("天数")
            days_dialog.setWindowTitle("请输入要分析的天数")
            days_dialog.setOkButtonText(u"确定")
            days_dialog.setCancelButtonText(u"取消")
            if days_dialog.exec_():
                days = days_dialog.intValue()

                t = threading.Thread(target=LiuAnalyze.LiuAnalyze.liu_stock_trend, args=(days,))
                t.setDaemon(True)
                t.start()
                self.log_msg("开始执行刘股票趋势分析")

    def analyze_ml_lstm_close_forcast(self):
        stock_code_dialog = QInputDialog()
        stock_code_dialog.setInputMode(0)
        stock_code_dialog.setLabelText("股票代码")
        stock_code_dialog.setWindowTitle("请输入股票代码")
        stock_code_dialog.setOkButtonText(u"确定")
        stock_code_dialog.setCancelButtonText(u"取消")

        if stock_code_dialog.exec_():
            try:
                stock_code = stock_code_dialog.textValue()
                t = threading.Thread(target=MLAnalyze.MLAnalyze.lstm_price_forcast, args=(stock_code,))
                t.setDaemon(True)
                t.start()

                msg = '开始执行代码为 %s 的股票LSTM股票收盘价预测分析' % stock_code
                self.log_msg(msg)


            except Exception as err:
                print(err)

    def analyze_ml_stock_info_clustering(self):
        try:
            msg = '开始执行股票信息无监督聚类'
            self.log_msg(msg)

            t = threading.Thread(target=MLAnalyze.MLAnalyze.stock_info_clustering())
            t.setDaemon(True)
            t.start()
        except Exception as err:
            print(err)


    def set_main_widget(self, widget):
        self.layout.removeWidget(self.last_main_widget)
        self.layout.removeWidget(self.log_msg_widget)
        self.layout.addWidget(widget)
        self.last_main_widget = widget
        self.layout.addWidget(self.log_msg_widget)
        self.layout.setStretchFactor(widget, 3)
        self.layout.setStretchFactor(self.log_msg_widget, 1)

    def log_msg(self, msg):
        msg = '%s：%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), msg)
        self.log_msg_widget.insertItem(0, msg)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PyQt5GUI()
    ex.showFullScreen()
    sys.exit(app.exec_())