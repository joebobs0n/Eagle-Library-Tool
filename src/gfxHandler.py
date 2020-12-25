#!/bin/usr/python3

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor, QPen
import numpy as np


grid_size = 50
grid_px = 25
mil_per_mm = 39.3701
size_conv = mil_per_mm * (grid_px / 50)


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
    origin_ends = grid_px/2
    scene.addLine(-origin_ends, 0, origin_ends, 0, originPen)
    scene.addLine(0, -origin_ends, 0, origin_ends, originPen)

    gridPen = QPen(QColor(*(app.gfx_theme['grid'])), 1)
    grid_ind = [i - int(np.floor(grid_size/2)) for i in list(range(grid_size + 1))]
    for x in grid_ind:
        for y in grid_ind:
            scene.addEllipse(y*grid_px-1, x*grid_px-1, 1, 1, gridPen)

    view.centerOn(0, 0)


def drawPin(app, scene, element):
    pass


def drawPad(app, scene, element):
    pass


def drawWire(app, scene, element):
    layer_color_obj = app.lib_obj.getLayers(number=element.attrib['layer'])
    layer_color = layer_color_obj.attrib['color']
    color = QColor(*(app.gfx_theme['colors'][layer_color]))
    width = np.floor(float(element.attrib['width'])*app.draw_conv)
    pen = QPen(color, width)
    xa = float(element.attrib['x1'])*size_conv
    xb = float(element.attrib['x2'])*size_conv
    ya = float(element.attrib['y1'])*size_conv
    yb = float(element.attrib['y2'])*size_conv

#! comment out 65 if using rounded corners code
    scene.addLine(xa, ya, xb, yb, pen)

# TODO: rounded ends on lines
    # try:
    #     m = (yb-ya)/(xb-xa)
    # except ZeroDivisionError:
    #     m = np.inf
    # theta = np.arctan(m)
    # r = width/2
    # x_delta = round(r*np.cos(theta))
    # y_delta = round(r*np.sin(theta))

    # x1 = y1 = x2 = y2 = 0
    # if ya == yb:
    #     if xa == xb:
    #         raise Exception('(x1, y2) == (x2, y2)', (xa, ya), (xb, yb))
    #     else:
    #         x1 = xa + x_delta if xa < xb else xb + x_delta
    #         y1 = ya + y_delta if xa < xb else yb + y_delta
    #         x2 = xa - x_delta if xa > xb else xb - x_delta
    #         y2 = ya - y_delta if xa > xb else yb - y_delta
    # else:
    #     if xa == xb:
    #         x1 = xa + x_delta if ya > yb else xb + x_delta
    #         y1 = ya + y_delta if ya > yb else yb + y_delta
    #         x2 = xa - x_delta if ya < yb else xb - x_delta
    #         y2 = ya - y_delta if ya < yb else yb - y_delta
    #     else:
    #         x1 = xa + x_delta if ya < yb else xb + x_delta
    #         y1 = ya + y_delta if ya < yb else yb + y_delta
    #         x2 = xa - x_delta if ya > yb else xb - x_delta
    #         y2 = ya - y_delta if ya > yb else yb - y_delta

    # scene.addLine(x1, y1, x2, y2, pen)
    # scene.addEllipse(x1-r/2, y1-r/2, r, r, pen)
    # scene.addEllipse(x2-r/2, y2-r/2, r, r, pen)


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