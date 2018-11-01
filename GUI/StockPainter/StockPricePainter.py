import pyqtgraph as pg
import tushare as ts

import time
import sys
from PyQt5.QtWidgets import *
import numpy
from pyqtgraph import AxisItem
from datetime import datetime, timedelta
from time import mktime
from GUI.StockPainter.DateAxisItem import *
from GUI.StockPainter.StockWindow import *


__all__ = ["DateAxisItem"]

class PriceLineItem(pg.GraphicsObject):
    def __init__(self, data):
        pg.GraphicsObject.__init__(self)
        self.data = data
        self.generatePicture()

    def generatePicture(self):
        self.picture = pg.QtGui.QPicture()
        p = pg.QtGui.QPainter(self.picture)
        p.setPen(pg.mkPen('r'))
        w = (self.data[1][0] - self.data[0][0]) / 3.

        i = 0
        data_len = len(self.data)
        while i < data_len - 1:
            first_point = self.data[i]
            second_point = self.data[i+1]


            p.drawLine(pg.QtCore.QPointF(first_point[0], first_point[2]), pg.QtCore.QPointF(second_point[0], second_point[2]))

            i = i + 1

        p.end()

    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        return pg.QtCore.QRectF(self.picture.boundingRect())

class StockPricePainter():
    @staticmethod
    def produce_basic_price_plot_widget(input_data):
        if input_data is None:
            return None

        data_list = []
        for i in range(len(input_data)):
            state_dt = input_data[i][0]
            stock_code = input_data[i][1]
            open = input_data[i][2]
            close = input_data[i][3]
            high = input_data[i][4]
            low = input_data[i][5]
            vol = input_data[i][6]
            amount = input_data[i][7]
            pre_close = input_data[i][8]
            amt_change = input_data[i][9]
            pct_change = input_data[i][10]

            date_time = datetime.strptime(state_dt, '%Y-%m-%d')
            t = time.mktime(date_time.timetuple())
            data = (t, open, close, low, high)
            data_list.append(data)

        item = PriceLineItem(data_list)
        plt = pg.PlotWidget()
        plt.setBackground('w')

        axis = DateAxisItem(orientation='bottom')
        axis.attachToPlotItem(plt.getPlotItem())

        plt.addItem(item, )
        plt.showGrid(x=True, y=True)
        return plt

    @staticmethod
    def produce_basic_price_windows(input_data, stock_code='K线图'):
        win = StockWindow()
        widget = StockPricePainter.produce_basic_price_plot_widget(input_data)
        win.create_window(1500, 800)
        win.init_UI(widget, stock_code)

        return win



