#!/bin/usr/python3

import src.lbrHandler as lh
from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import webbrowser as web
from pathlib import Path
import os
import sys

os.chdir(sys.path[0])

class EagleToolApp(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('src/main.ui', self)
        self.setWindowIcon(QtGui.QIcon('bin/icon.png'))

        self.export_menuitem.setEnabled(False)
        self.exportas_menuitem.setEnabled(False)
        self.close_menuitem.setEnabled(False)

        self.load_menuitem.triggered.connect(self.openLbr)
        self.export_menuitem.triggered.connect(self.exportLbr)
        self.exportas_menuitem.triggered.connect(self.exportAsLbr)
        self.close_menuitem.triggered.connect(self.closeLbr)
        self.exit_menuitem.triggered.connect(self.exitProgram)
        self.userdefined_menuitem.triggered.connect(self.userDefinedTool)
        self.nameprefix_menuitem.triggered.connect(self.namePrefixTool)
        self.merge_menuitem.triggered.connect(self.mergeTool)
        self.github_menuitem.triggered.connect(self.githubPage)
        self.readme_menuitem.triggered.connect(self.showREADME)
        self.contact_menuitem.triggered.connect(self.contactMe)

        self.device_list.itemSelectionChanged.connect(self.deviceSelected)
        self.variant_list.itemSelectionChanged.connect(self.variantSelected)

    def openLbr(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, "Import Eagle Library File", "","All Files (*);;Eagle Libraries (*.lbr)", options=options)
        filename_path = Path(filename)
        if filename:
            if Path(filename).suffixes[0] == '.lbr':
                print(filename)
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

    def closeLbr(self):
        confirm = QMessageBox.warning(self, 'Close Out Library?', 'Are you sure that you want to close out the current working library?', QMessageBox.Yes | QMessageBox.Save | QMessageBox.Cancel, QMessageBox.Cancel)
        closeOut = False
        if confirm == QMessageBox.Yes:
            closeOut = True
        elif confirm == QMessageBox.Save:
            self.exportLbr()
            closeOut = True

        if closeOut == True:
            self.filename = None
            self.device_list.clear()
            self.variant_list.clear()
            self.lib_obj = None
            self.connection_footnotes.setText('')
            self.footprint_footnotes.setText('')
            self.symbol_footnotes.setText('')

            self.export_menuitem.setEnabled(False)
            self.exportas_menuitem.setEnabled(False)
            self.close_menuitem.setEnabled(False)

            self.status_label.setText('<html><head/><body><p><span style=" color:#ff0000;">No Library Loaded</span></p></body></html>')

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
        self.connection_footnotes.setText(device_message_temp)

    def setFootprintFootnotes(self):
        if len(self.selected_variant_obj) > 0:
            footprint_message_temp = ''
            dev, ftp = self.selected_variant_obj
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

    def variantSelected(self):
        self.selected_variant_name = self.variant_list.currentItem().text()
        self.selected_variant_obj = self.lib_obj.getFootprints(self.selected_device_obj, self.selected_variant_name)
        self.setConnectionFootnotes()
        self.setFootprintFootnotes()

    def populateList(self, list):
        if list == 'devices':
            self.device_list.clear()
            self.device_objs = self.lib_obj.getDevices()
            for device in self.device_objs:
                self.device_list.addItem(device.attrib['name'])
        elif list == 'variants':
            self.variant_list.clear()
            self.variant_objs = self.lib_obj.getFootprints(self.selected_device_obj)
            for variant in self.variant_objs:
                _, ftp = variant
                self.variant_list.addItem(ftp.attrib['name'])