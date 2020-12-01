#!/usr/bin/python3

from src.app import EagleToolApp
from PyQt5 import QtWidgets
import sys

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    win = EagleToolApp()
    win.show()
    sys.exit(app.exec_())
