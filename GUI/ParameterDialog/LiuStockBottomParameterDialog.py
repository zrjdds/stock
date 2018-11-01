#coding=utf-8

import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import numpy as np

#from PyQt5.QtWidgets import QApplication, QDialog,QWidget, QFontDialog, QPushButton, QLineEdit, QGridLayout, QLabel, QDialogButtonBox

from PyQt5.QtWidgets import *

class LiuStockBottomParameterDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.resize(200, 140)
        self.setWindowTitle('请输入参数')

        grid = QGridLayout()

        grid.addWidget(QLabel('分析所用的数据天数', parent=self), 0, 0, 1, 1)

        self.days = QLineEdit(parent=self)
        self.days.setText("180")
        grid.addWidget(self.days, 0, 1, 1, 1)

        grid.addWidget(QLabel('最大允许波动价格比例', parent=self), 1, 0, 1, 1)

        self.offset = QLineEdit(parent=self)
        self.offset.setText("10")
        grid.addWidget(self.offset, 1, 1, 1, 1)

        grid.addWidget(QLabel('最小下跌倍数', parent=self), 2, 0, 1, 1)
        self.ratio = QLineEdit(parent=self)
        self.ratio.setText("3")
        grid.addWidget(self.ratio, 2, 1, 1, 1)


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
    dialog = LiuStockBottomParameterDialog()
    if dialog.exec_():
        try:
            days = int(dialog.days.text())
            offset = int(dialog.offset.text())
            ratio = int(dialog.ratio.text())

            print(days)
            print(offset)
            print(ratio)

        except Exception as err:
            print(err)
