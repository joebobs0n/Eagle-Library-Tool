#!/bin/usr/python3

import src.lbrHandler as lh
from src.helpers import EagleVisuals as ev

from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QBrush, QPen, QColor, QFont
from PyQt5.QtCore import Qt
from pathlib import Path
import webbrowser as web
import numpy as np
import os
import sys
import json

os.chdir(sys.path[0])

class EagleToolApp(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('src/main.ui', self)
        self.setWindowIcon(QtGui.QIcon('bin/icon.png'))

        self.export_menuitem.setEnabled(False)
        self.exportas_menuitem.setEnabled(False)
        self.close_menuitem.setEnabled(False)

        self.initTriggers()
        self.initSettings()
        self.initGfx()

    def initTriggers(self):
        self.load_menuitem.triggered.connect(self.openLbr)
        self.export_menuitem.triggered.connect(self.exportLbr)
        self.exportas_menuitem.triggered.connect(self.exportAsLbr)
        self.close_menuitem.triggered.connect(self.closeLbr)
        self.exit_menuitem.triggered.connect(self.exitProgram)
        self.uservalue_menuitem.triggered.connect(self.userDefinedTool)
        self.nameprefix_menuitem.triggered.connect(self.namePrefixTool)
        self.merge_menuitem.triggered.connect(self.mergeTool)
        self.github_menuitem.triggered.connect(self.githubPage)
        self.readme_menuitem.triggered.connect(self.showREADME)
        self.contact_menuitem.triggered.connect(self.contactMe)
        self.about_menuitem.triggered.connect(self.about)

        self.device_list.itemSelectionChanged.connect(self.deviceSelected)
        self.footprint_list.itemSelectionChanged.connect(self.variantSelected)

    def initSettings(self):
        if Path('config/settings.json').exists():
            with open('config/settings.json') as f:
                self.settings = json.load(f)

        gfx_theme_path = f'themes/gfx_{self.settings["gfx_theme"]}.json'
        if Path(gfx_theme_path).exists():
            with open(gfx_theme_path) as f:
                self.gfx_theme = json.load(f)
        else:
            with open('themes/gfx_dark.json') as f:
                self.gfx_theme = json.load(f)

    def initGfx(self):
        self.backgroundColor = QColor(*(self.gfx_theme['background']))

        self.footprint_scene = QGraphicsScene(self)
        # self.footprint_scene.setSceneRect(-245, -245, 490, 490)
        self.footprint_gfx.setScene(self.footprint_scene)

        self.symbol_scene = QGraphicsScene(self)
        # self.symbol_scene.setSceneRect(-245, -245, 490, 490)
        self.symbol_gfx.setScene(self.symbol_scene)

        self.resetGfx(self.footprint_scene, self.footprint_gfx)
        self.resetGfx(self.symbol_scene, self.symbol_gfx)

    def resetGfx(self, scene, view):
        scene.clear()
        scene.setBackgroundBrush(QBrush(self.backgroundColor))
        scene.addLine(-10, 0, 10, 0, QPen(QColor(*(self.gfx_theme['origin'])), 2))
        scene.addLine(0, -10, 0, 10, QPen(QColor(*(self.gfx_theme['origin'])), 2))

        for x in np.linspace(-250, 250, 51):
            for y in np.linspace(-250, 250, 51):
                scene.addEllipse(x-1, y-1, 1, 1, QPen(QColor(*(self.gfx_theme['grid']))))

        view.centerOn(0, 0)

    def openLbr(self):
        self.closeLbr(prompt=False)
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, "Import Eagle Library File", "","All Files (*);;Eagle Libraries (*.lbr)", options=options)
        filename_path = Path(filename)
        if filename:
            if Path(filename).suffixes[0] == '.lbr':
                self.filename = filename
                self.lib_obj = lh.EagleLibrary(self.filename)
                self.status_label.setText(Path(self.filename).name)
                self.populateList('devices')
                self.export_menuitem.setEnabled(True)
                self.exportas_menuitem.setEnabled(True)
                self.close_menuitem.setEnabled(True)

    def exportLbr(self):
        print('selected exportlbr')

    def exportAsLbr(self):
        print('selected exportAsLbr')

    def closeLbr(self, prompt=True):
        if prompt:
            confirm = QMessageBox.warning(self, 'Close Out Library?', 'Are you sure that you want to close out the current working library?', QMessageBox.Yes | QMessageBox.Save | QMessageBox.Cancel, QMessageBox.Cancel)
            closeOut = False
            if confirm == QMessageBox.Yes:
                closeOut = True
            elif confirm == QMessageBox.Save:
                self.exportLbr()
                closeOut = True
        else:
            closeOut = True

        if closeOut == True:
            self.filename = None
            self.device_list.clear()
            self.footprint_list.clear()
            self.lib_obj = None
            self.device_footnotes.setText('')
            self.footprint_footnotes.setText('')
            self.symbol_footnotes.setText('')

            self.export_menuitem.setEnabled(False)
            self.exportas_menuitem.setEnabled(False)
            self.close_menuitem.setEnabled(False)

            self.resetGfx(self.footprint_scene, self.footprint_gfx)
            self.resetGfx(self.symbol_scene, self.symbol_gfx)

            self.status_label.setText('<html><head/><body><p><span style="color:#ff0000;">No Library Loaded</span></p></body></html>')

    def exitProgram(self):
        QtWidgets.QApplication.quit()

    def userDefinedTool(self):
        print('selected userDefinedTool')

    def namePrefixTool(self):
        print('selected namePrefixTool')

    def mergeTool(self):
        print('selected mergeTool')

    def githubPage(self):
        web.open('https://github.com/joebobs0n/Eagle-Library-Tool/')

    def showREADME(self):
        print('selected showREADME')

    def contactMe(self):
        QMessageBox.information(self, 'Contact Info', 'Name: Andy Monk\nEmail: czech.monk90@gmail.com', QMessageBox.Close, QMessageBox.Close)

    def about(self):
        QMessageBox.about(self, 'About Eagle Library Tool', 'The Eagle Library Tool (perhaps come up with a cooler name?) is an Open Source tool provided under the MIT license.')

    def setConnectionFootnotes(self):
        self.connections = []
        try:
            self.connections = self.lib_obj.getConnections(self.selected_device_obj, self.variant_list.currentItem().text())
            if len(self.connections) == 0:
                self.connections = self.lib_obj.getConnections(self.selected_device_obj)
        except:
            self.connections = self.lib_obj.getConnections(self.selected_device_obj)

        device_message_temp = ''
        for connection in self.connections:
            device_message_temp += f'{self.lib_obj.printLibraryStructure(connection)}\n'
        self.device_footnotes.setText(device_message_temp)

    def setFootprintFootnotes(self):
        if len(self.selected_variant_obj) > 0:
            footprint_message_temp = ''
            dev, ftp = self.selected_variant_obj
            variant_name = dev.attrib['name'] if dev.attrib['name'] != '' else '<no variant name>'
            footprint_message_temp += f'Variant name: {variant_name}\n'
            footprint_message_temp += f'{self.lib_obj.printLibraryStructure(ftp)}\n'
            self.footprint_footnotes.setText(footprint_message_temp)
        else:
            device_variants = self.lib_obj.getFootprints(self.selected_device_obj)
            footprint_message_temp = ''
            for variant in device_variants:
                dev, ftp = variant
                variant_name = dev.attrib['name'] if dev.attrib['name'] != '' else '<no variant name>'
                footprint_message_temp += f'Variant name: {variant_name}\n'
                footprint_message_temp += f'{self.lib_obj.printLibraryStructure(ftp)}\n'
            if footprint_message_temp != '':
                self.footprint_footnotes.setText(footprint_message_temp)
            else:
                self.footprint_footnotes.setText('Symbol only part (typically supply symbols)')

    def setSymbolFootnotes(self):
        symbol_message_temp = ''
        for symbol in self.selected_symbol_objs:
            gate, sym = symbol
            symbol_message_temp += f'Gate name: {gate.attrib["name"]}\n'
            symbol_message_temp += f'{self.lib_obj.printLibraryStructure(sym)}\n'
        self.symbol_footnotes.setText(symbol_message_temp)

    def deviceSelected(self):
        self.selected_device_name = self.device_list.currentItem().text()
        self.selected_device_obj = self.lib_obj.getDevices(self.selected_device_name)
        self.selected_variant_obj = []
        self.selected_symbol_objs = self.lib_obj.getSymbols(self.selected_device_obj)

        self.setConnectionFootnotes()
        self.setFootprintFootnotes()
        self.setSymbolFootnotes()

        self.populateList('variants')

        self.drawSymbol()

    def variantSelected(self):
        self.selected_variant_name = self.footprint_list.currentItem().text()
        self.selected_variant_obj = self.lib_obj.getFootprints(self.selected_device_obj, self.selected_variant_name)
        self.setConnectionFootnotes()
        self.setFootprintFootnotes()

        self.drawFootprint()

    def populateList(self, list):
        if list == 'devices':
            self.device_list.clear()
            self.device_objs = self.lib_obj.getDevices()
            for device in self.device_objs:
                self.device_list.addItem(device.attrib['name'])
            if self.settings['lists_autoselect_first']:
                self.device_list.setCurrentRow(0)
        elif list == 'variants':
            self.footprint_list.clear()
            self.variant_objs = self.lib_obj.getFootprints(self.selected_device_obj)
            for variant in self.variant_objs:
                _, ftp = variant
                self.footprint_list.addItem(ftp.attrib['name'])
            if self.settings['lists_autoselect_first']:
                self.footprint_list.setCurrentRow(0)

    def drawSymbol(self):
        # self.resetGfx(self.symbol_scene, self.symbol_gfx)
        # if self.settings['gfx_display_name']:
        #     symbolNames = [obj[1].attrib['name'] for obj in self.selected_symbol_objs]
        #     for idx, name in enumerate(symbolNames):
        #         text = self.symbol_scene.addText(name)
        #         text.setPos(-245, -245 + idx*12)
        #         text.setDefaultTextColor(ev.layerColors['4'])
        pass

    def drawFootprint(self):
        # self.resetGfx(self.footprint_scene, self.footprint_gfx)
        # if self.settings['gfx_display_name']:
        #     try:
        #         footprintName = self.selected_variant_obj[1].attrib['name']
        #         text = self.footprint_scene.addText(footprintName)
        #         text.setPos(-245, -245)
        #         text.setDefaultTextColor(ev.layerColors['4'])
        #     except:
        #         pass
        pass