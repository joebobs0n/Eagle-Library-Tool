#!/bin/usr/python3

import src.beHandler as be
import src.gfxHandler as gfx
import src.helpers as helpers

from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import QGraphicsScene, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import QColor

from pathlib import Path
import webbrowser as web
import json
import os
import sys

os.chdir(sys.path[0])

class EagleToolApp(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('src/main.ui', self)
        self.setWindowIcon(QtGui.QIcon('bin/icon.png'))

        self.__initTriggers()
        self.__initSettings()
        self.__initGfx()

        self.current_filename = None
        self.current_savefile = None
        self.unsaved_changes = False

    def __initTriggers(self):
        self.load_menuitem.triggered.connect(self.__openLbr)
        self.export_menuitem.triggered.connect(self.__exportLbr)
        self.exportas_menuitem.triggered.connect(self.__exportAsLbr)
        self.close_menuitem.triggered.connect(self.__closeLbr)
        self.exit_menuitem.triggered.connect(self.__exitProgram)
        self.uservalue_menuitem.triggered.connect(self.__userValueTool)
        self.nameprefix_menuitem.triggered.connect(self.__namePrefixTool)
        self.merge_menuitem.triggered.connect(self.__mergeTool)
        self.github_menuitem.triggered.connect(self.__githubPage)
        self.readme_menuitem.triggered.connect(self.__showREADME)
        self.contact_menuitem.triggered.connect(self.__contactMe)
        self.about_menuitem.triggered.connect(self.__about)

        self.device_list.itemSelectionChanged.connect(self.__deviceSelected)
        self.footprint_list.itemSelectionChanged.connect(self.__footprintSelected)

    def __initSettings(self):
        with open('config/settings.json') as f:
            self.settings = json.load(f)

        gfx_path = 'themes/gfx_dark.json'
        gfx_theme_select = self.settings['gfx_theme']
        if gfx_theme_select == 'dark' or gfx_theme_select == 'light':
            gfx_path = f'themes/gfx_{gfx_theme_select}.json'
        else:
            path_check = f'config/gfx_{gfx_theme_select}.json'
            if Path(path_check).exists():
                gfx_path = path_check
        gfx_path = Path(gfx_path)

        with open(gfx_path, 'r') as f:
            self.gfx_theme = json.load(f)

    def __initGfx(self):
        self.gfx_backgroundColor = QColor(*(self.gfx_theme['background']))

        self.footprint_scene = QGraphicsScene(self)
        self.footprint_gfx.setScene(self.footprint_scene)
        gfx.reset(self, self.footprint_scene, self.footprint_gfx)

        self.symbol_scene = QGraphicsScene(self)
        self.symbol_gfx.setScene(self.symbol_scene)
        gfx.reset(self, self.symbol_scene, self.symbol_gfx)

    def __openLbr(self):
        self.__closeLbr()
        self.current_filename, _ = QFileDialog.getOpenFileName(self, "Select Eagle Library File", "", "All Files (*);;Eagle Libraries (*.lbr)")
        be.open(self, self.current_filename)

    def __exportLbr(self):
        if self.current_savefile == None:
            self.__exportAsLbr()
        else:
            be.save(self, self.current_savefile)

    def __exportAsLbr(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Library As", "", "All Files (*);;Eagle Libraries (*.lbr)", "Eagle Libraries (*.lbr)")
        be.save(self, filename)

    def __closeLbr(self):
        status = ''
        if self.unsaved_changes:
            confirm = QMessageBox.warning(self, 'Close Out Library?', 'There are unsaved changes in the current working Library.\nAre you sure that you want to close out the current working library?', QMessageBox.Yes | QMessageBox.Save | QMessageBox.Cancel, QMessageBox.Cancel)
            closeOut = False
            if confirm == QMessageBox.Yes:
                closeOut = True
                status = 'unsaved'
            elif confirm == QMessageBox.Save:
                self.__exportLbr()
                closeOut = True
                status = 'saved'
            else:
                status = 'cancelled'
        else:
            closeOut = True

        if closeOut == True:
            be.close(self)

        return status

    def closeEvent(self, evt):
        if self.unsaved_changes:
            confirm = QMessageBox.warning(self, 'Exit Without Saving?', 'There are unsaved changes in the current working library.', QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel, QMessageBox.Cancel)
            if confirm == QMessageBox.Save:
                self.__exportLbr()
            elif confirm == QMessageBox.Cancel:
                evt.ignore()

    def __exitProgram(self):
        self.close()

    def __userValueTool(self):
        print('selected set uservalue tool')

    def __namePrefixTool(self):
        print('selected set prefix tool')

    def __mergeTool(self):
        print('selected library merge tool')

    def __githubPage(self):
        web.open('https://github.com/joebobs0n/Eagle-Library-Tool')

    def __showREADME(self):
        print('selected README')

    def __contactMe(self):
        QMessageBox.information(self, 'Contact Info', 'Name: Andy Monk\nEmail: czech.monk90@gmail.com', QMessageBox.Close, QMessageBox.Close)

    def __about(self):
        QMessageBox.about(self, 'About Eagle Library Tool', 'The Eagle Library Tool (perhaps come up with a cooler name?) is an Open Source tool provided under the MIT license.')

    def __deviceSelected(self):
        gfx.reset(self, self.symbol_scene, self.symbol_gfx)
        gfx.reset(self, self.footprint_scene, self.footprint_gfx)

        selected_device_name = self.device_list.currentItem().text()
        self.selected_device_obj = self.lib_obj.getDevices(selected_device_name)
        self.selected_footprint_obj = []
        self.selected_symbol_objs = self.lib_obj.getSymbols(self.selected_device_obj)

        be.setDeviceFootnotes(self)
        be.setFootprintFootnotes(self)
        be.setSymbolFootnotes(self)

        be.populateList(self, 'footprints')

        gfx.drawSymbol(self, self.symbol_scene, self.symbol_gfx)

    def __footprintSelected(self):
        gfx.reset(self, self.footprint_scene, self.footprint_gfx)

        selected_footprint_name = self.footprint_list.currentItem().text()
        self.selected_footprint_obj = self.lib_obj.getFootprints(self.selected_device_obj, selected_footprint_name)

        be.setDeviceFootnotes(self)
        be.setFootprintFootnotes(self)

        if len(self.selected_footprint_obj) == 1:
            gfx.drawFootprint(self, self.footprint_scene, self.footprint_gfx)

