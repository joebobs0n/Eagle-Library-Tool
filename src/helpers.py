#!/bin/usr/python3

from PyQt5.QtGui import QBrush, QPen, QColor
from PyQt5.QtCore import Qt

class EagleVisuals:
    colors = {
        '1': [10, 125, 177],
        '2': [54, 181, 126],
        '3': [45, 165, 165],
        '4': [166, 15, 15],
        '5': [209, 154, 11],
        '6': [165, 165, 45],
        '7': [165, 165, 165],
        '8': [36, 36, 36],
        '9': [8, 8, 188],
        '10': [8, 188, 8],
        '11': [8, 188, 188],
        '12': [209, 5, 5],
        '13': [209, 5, 209],
        '14': [209, 169, 11],
        '15': [145, 172, 47],
        '16': [209, 190, 66],
        '17': [121, 172, 101],
        '18': [209, 182, 134],
        '19': [81, 143, 74],
        '20': [5, 158, 147],
        '21': [86, 183, 198],
        '22': [163, 80, 135],
        '23': [201, 85, 23],
        '24': [195, 163, 59],
        '25': [80, 115, 104],
        '26': [94, 60, 149],
        '27': [70, 84, 84],
        '28': [176, 135, 143],
        '29': [196, 62, 94],
        '30': [175, 181, 209]
    }

    fill = {
        '1': Qt.SolidPattern,
        '2': Qt.HorPattern,
        '3': Qt.BDiagPattern,
        '4': Qt.BDiagPattern,
        '5': Qt.FDiagPattern,
        '6': Qt.FDiagPattern,
        '7': Qt.CrossPattern,
        '8': Qt.DiagCrossPattern,
        '9': Qt.Dense4Pattern,
        '10': Qt.Dense7Pattern,
        '11': Qt.Dense6Pattern,
        '12': Qt.Dense5Pattern
    }