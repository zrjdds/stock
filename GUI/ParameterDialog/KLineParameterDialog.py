#coding=utf-8

import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import numpy as np
import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDate, QTime, QDateTime, Qt


class KLineParameterDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.resize(200, 140)
        self.setWindowTitle('请输入参数')

        grid = QGridLayout()

        grid.addWidget(QLabel('股票编号', parent=self), 0, 0, 1, 1)

        self.stock_code = QLineEdit(parent=self)
        self.stock_code.setText("000939.SZ")
        grid.addWidget(self.stock_code, 0, 1, 1, 1)

        grid.addWidget(QLabel('开始时间', parent=self), 1, 0, 1, 1)
        self.start_calendar = QCalendarWidget(self)
        self.start_calendar.setSelectedDate(datetime.datetime.now() - datetime.timedelta(days=180))
        grid.addWidget(self.start_calendar, 1, 1, 1, 1)

        grid.addWidget(QLabel('结束时间', parent=self), 2, 0, 1, 1)
        self.end_calendar = QCalendarWidget(self)
        grid.addWidget(self.end_calendar, 2, 1, 1, 1)

        buttonBox = QDialogButtonBox(parent=self)
        buttonBox.setOrientation(QtCore.Qt.Horizontal)  # 设置为水平方向
        buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)  # 确定和取消两个按钮
        buttonBox.button(QDialogButtonBox.Ok).setText("确定")
        buttonBox.button(QDialogButtonBox.Cancel).setText("取消")
        buttonBox.accepted.connect(self.accept)  # 确定
        buttonBox.rejected.connect(self.reject)  # 取消
        layout = QVBoxLayout()
        layout.addLayout(grid)
        spacerItem = QSpacerItem(20, 48, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacerItem)
        layout.addWidget(buttonBox)
        self.setLayout(layout)

        def closeEvent(self, event):
            reply = QMessageBox.question(self, 'Close Message',
                                         "Are you sure to quit?", QtGui.QMessageBox.Yes |
                                         QtGui.QMessageBox.No, QtGui.QMessageBox.No)
            if reply == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()


if __name__ == '__main__':
    app = QApplication([])
    dialog = KLineParameterDialog()
    if dialog.exec_():
        try:
            pass

        except Exception as err:
            print(err)
