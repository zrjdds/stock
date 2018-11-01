#coding=utf-8

import sys
from PyQt5.QtWidgets import *
from GUI import PyQt5GUI

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PyQt5GUI.PyQt5GUI()
    ex.show()
    sys.exit(app.exec_())