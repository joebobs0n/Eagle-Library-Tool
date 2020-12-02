#!/bin/usr/python3

from PyQt5.QtGui import QBrush, QPen, QColor
from PyQt5.QtCore import Qt

class EagleVisuals:
    layerColors = {
        '1': QColor(255, 0, 0),
        '2': QColor(0, 255, 0),
        '3': QColor(0, 0, 255),
        '4': QColor(255, 255, 255),
        '5': QColor(0, 0, 0),
        '6': QColor(0, 0, 0),
        '7': QColor(0, 0, 0),
        '8': QColor(0, 0, 0),
        '9': QColor(0, 0, 0),
        '10': QColor(0, 0, 0),
        '11': QColor(0, 0, 0),
        '12': QColor(0, 0, 0),
        '13': QColor(0, 0, 0),
        '14': QColor(0, 0, 0),
        '15': QColor(0, 0, 0),
        '16': QColor(0, 0, 0),
        '17': QColor(0, 0, 0),
        '18': QColor(0, 0, 0),
        '19': QColor(0, 0, 0),
        '20': QColor(0, 0, 0),
        '21': QColor(0, 0, 0),
        '22': QColor(0, 0, 0),
        '23': QColor(0, 0, 0),
        '24': QColor(0, 0, 0),
        '25': QColor(0, 0, 0),
        '26': QColor(0, 0, 0),
        '27': QColor(0, 0, 0),
        '28': QColor(0, 0, 0),
        '29': QColor(0, 0, 0),
        '30': QColor(0, 0, 0)
    }

    brushes = {
        'solid': QBrush(Qt.SolidPattern),
        'sparce dots': QBrush(Qt.Dense1Pattern),
        'tight dots': QBrush(Qt.Dense3Pattern),
        'light dots': QBrush(Qt.Dense6Pattern),
        'back diag': QBrush(Qt.BDiagPattern),
        'front diag': QBrush(Qt.FDiagPattern),
        'criss cross': QBrush(Qt.DiagCrossPattern)
    }