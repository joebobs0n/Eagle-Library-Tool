#!/usr/bin/python3

import src.lbrHandler as lh
import src.gfxHandler as gfx

from PyQt5 import QtWidgets

from pathlib import Path

def open(app, filename):
    if filename:
        filename_path = Path(filename)
        if filename_path.exists() and filename_path.suffixes[0] == '.lbr':
            app.lib_obj = lh.EagleLibrary(filename)
            app.status_label.setText(filename_path.name)

            app.export_menuitem.setEnabled(True)
            app.exportas_menuitem.setEnabled(True)
            app.close_menuitem.setEnabled(True)

            if app.settings['save_opened_as_same_file']:
                app.current_savefile = filename
                app.unsaved_changes = False
            else:
                app.current_savefile = None
                app.unsaved_changes = True

            # app.populateList('devices')

def save(app, filename):
    if filename:
        filename_path = Path(filename)
        if filename != '' and filename_path.suffixes[0] == '.lbr':
            app.unsaved_changes = False
            app.current_savefile = filename
            app.lib_obj.exportLibrary(app.current_savefile)

def close(app):
    app.current_filename = None
    app.current_savefile = None

    app.device_list.clear()
    app.variant_list.clear()
    app.connection_footnotes.clear()
    app.footprint_footnotes.clear()
    app.symbol_footnotes.clear()

    app.export_menuitem.setEnabled(False)
    app.exportas_menuitem.setEnabled(False)
    app.close_menuitem.setEnabled(False)

    gfx.reset(app, app.footprint_scene, app.footprint_gfx)
    gfx.reset(app, app.symbol_scene, app.symbol_gfx)

    app.status_label.setText('<html><head/><body><p><span style="color:#ff0000;">No Library Loaded</span></p></body></html>')

    app.lib_obj = None

def exit(app):
    QtWidgets.QApplication.quit()

