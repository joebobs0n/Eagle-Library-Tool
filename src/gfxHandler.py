#!/bin/usr/python3

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor, QPen

def reset(app, scene, view):
    scene.clear()
    scene.setBackgroundBrush(QBrush(app.gfx_backgroundColor))
    originPen = QPen(QColor(*(app.gfx_theme['origin'])), 2)
    scene.addLine(-10, 0, 10, 0, originPen)
    scene.addLine(0, -10, 0, 10, originPen)

    # add grid here

    scene.addRect(-100, -100, 200, 200, QPen(QColor(Qt.white)), QBrush(QColor(Qt.white), Qt.BDiagPattern))

    view.centerOn(0, 0)
