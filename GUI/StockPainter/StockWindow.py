#coding=utf-8
import pyqtgraph as pg
import tushare as ts

import time
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class StockWindow(QMainWindow):
    def __init__(self):
        super(StockWindow, self).__init__()

    def create_window(self, window_width, window_height):
        parent = None
        super(StockWindow, self).__init__(parent)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.resize(window_width, window_height)
        #self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowModality(Qt.WindowModal)

    def init_UI(self, widget, title):
        self.setWindowTitle(title)
        self.setCentralWidget(widget)
