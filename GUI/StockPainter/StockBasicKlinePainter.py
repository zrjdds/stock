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

class CandlestickItem(pg.GraphicsObject):
    def __init__(self, data):
        pg.GraphicsObject.__init__(self)
        self.data = data  ## data must have fields: time, open, close, min, max
        self.generatePicture()

    def generatePicture(self):
        self.picture = pg.QtGui.QPicture()
        p = pg.QtGui.QPainter(self.picture)
        p.setPen(pg.mkPen('b'))
        w = (self.data[1][0] - self.data[0][0]) / 3.
        for (t, open, close, min, max) in self.data:
            p.drawLine(pg.QtCore.QPointF(t, min), pg.QtCore.QPointF(t, max))
            if open > close:
                p.setBrush(pg.mkBrush('g'))
            else:
                p.setBrush(pg.mkBrush('r'))
            p.drawRect(pg.QtCore.QRectF(t - w, open, w * 2, close - open))
        p.end()

    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        return pg.QtCore.QRectF(self.picture.boundingRect())

class StockBasicKlinePainter():
    @staticmethod
    def produce_basic_kline_plot_widget(hist_data):
        if hist_data is None:
            return None

        data_list = []
        for i in range(len(hist_data)):
            state_dt = hist_data[i][0]
            stock_code = hist_data[i][1]
            open = hist_data[i][2]
            close = hist_data[i][3]
            high = hist_data[i][4]
            low = hist_data[i][5]
            vol = hist_data[i][6]
            amount = hist_data[i][7]
            pre_close = hist_data[i][8]
            amt_change = hist_data[i][9]
            pct_change = hist_data[i][10]

            date_time = datetime.strptime(state_dt, '%Y-%m-%d')
            t = time.mktime(date_time.timetuple())
            data = (t, open, close, low, high)
            data_list.append(data)

        item = CandlestickItem(data_list)
        plt = pg.PlotWidget()
        plt.setBackground('w')

        axis = DateAxisItem(orientation='bottom')
        axis.attachToPlotItem(plt.getPlotItem())

        plt.addItem(item, )
        plt.showGrid(x=True, y=True)
        return plt

    @staticmethod
    def produce_basic_kline_windows(hist_data, stock_code='K线图'):
        win = StockWindow()
        widget = StockBasicKlinePainter.produce_basic_kline_plot_widget(hist_data)
        win.create_window(800, 600)
        win.init_UI(widget, stock_code)

        return win



