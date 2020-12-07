#!/bin/usr/python3

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor, QPen
import numpy as np

grid_size = 50

def setGrid(app):
    grid = app.lib_obj.getElement('grid')[0]
    app.grid_scale = int(grid.attrib['distance'])
    unit_dist = grid.attrib['unitdist']
    unit = grid.attrib['unit']
    if unit_dist != unit:
        if unit_dist == 'mil':
            app.draw_conv = 39.3707874
        else:
            app.draw_conv = 0.0254
    else:
        app.draw_conv = 1

    print(app.grid_scale, app.draw_conv)


def reset(app, scene, view):
    scene.clear()
    scene.setBackgroundBrush(QBrush(app.gfx_backgroundColor))

    originPen = QPen(QColor(*(app.gfx_theme['origin'])), 2)
    origin_ends = 25
    scene.addLine(-origin_ends, 0, origin_ends, 0, originPen)
    scene.addLine(0, -origin_ends, 0, origin_ends, originPen)

    gridPen = QPen(QColor(*(app.gfx_theme['grid'])), 1)
    grid_ind = [i - int(np.floor(grid_size/2)) for i in list(range(grid_size + 1))]
    for x in grid_ind:
        for y in grid_ind:
            scene.addEllipse(y*grid_size/2-1, x*grid_size/2-1, 1, 1, gridPen)

    view.centerOn(0, 0)

def drawPin(app, scene, element):
    pass

def drawPad(app, scene, element):
    pass

def drawWire(app, scene, element):
    layer_color_obj = app.lib_obj.getLayers(number=element.attrib['layer'])
    layer_color = layer_color_obj.attrib['color']
    color = QColor(*(app.gfx_theme['colors'][layer_color]))
    width = round(float(element.attrib['width'])*app.draw_conv)
    pen = QPen(color, width)
    x1 = round(float(element.attrib['x1'])*app.draw_conv)
    x2 = round(float(element.attrib['x2'])*app.draw_conv)
    y1 = round(float(element.attrib['y1'])*app.draw_conv)
    y2 = round(float(element.attrib['y2'])*app.draw_conv)
    scene.addLine(x1, y1, x2, y2, pen)

def drawText(app, scene, element):
    pass

def drawCircle(app, scene, element):
    pass

def drawSymbol(app, scene, view):
    for symbol in app.selected_symbol_objs:
        gate, sym = symbol

def drawFootprint(app, scene, view):
    dev, ftp = app.selected_footprint_obj[0]
    dev_list = list(dev)
    ftp_list = list(ftp)

    for item in ftp_list:
        if item.tag == 'wire':
            drawWire(app, scene, item)