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

            gfx.setGrid(app)

            populateList(app, 'devices')

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
    app.footprint_list.clear()
    app.device_footnotes.clear()
    app.footprint_footnotes.clear()
    app.symbol_footnotes.clear()

    app.export_menuitem.setEnabled(False)
    app.exportas_menuitem.setEnabled(False)
    app.close_menuitem.setEnabled(False)

    # gfx.reset(app, app.footprint_scene, app.footprint_gfx)
    # gfx.reset(app, app.symbol_scene, app.symbol_gfx)

    app.status_label.setText('<html><head/><body><p><span style="color:#ff0000;">No Library Loaded</span></p></body></html>')

    app.lib_obj = None

def populateList(app, list):
    if list == 'devices':
        app.device_list.clear()
        app.device_objs = app.lib_obj.getDevices()
        for device in app.device_objs:
            app.device_list.addItem(device.attrib['name'])

        if app.settings['lists_autoselect_first']:
            app.device_list.setCurrentRow(0)
    elif list == 'footprints':
        app.footprint_list.clear()
        app.footprint_objs = app.lib_obj.getFootprints(app.selected_device_obj)
        for footprint in app.footprint_objs:
            _, ftp = footprint
            app.footprint_list.addItem(ftp.attrib['name'])

        if app.settings['lists_autoselect_first']:
            app.footprint_list.setCurrentRow(0)

def setDeviceFootnotes(app):
    app.connections = []
    try:
        connections = app.lib_obj.getConnections(app.selected_device_obj, app.footprint_list.currentItem().text())
        if len(connections) == 0:
            connections = app.lib_obj.getConnections(app.selected_device_obj)
    except:
        connections = app.lib_obj.getConnections(app.selected_device_obj)

    device_message = ''
    for connection in connections:
        device_message += f'{app.lib_obj.printLibraryStructure(connection)}\n'
    app.device_footnotes.setText(device_message)

def setFootprintFootnotes(app):
    if len(app.selected_footprint_obj) > 0:
        footprint_message = ''
        dev, ftp = app.selected_footprint_obj[0]
        variant_name = dev.attrib['name'] if dev.attrib['name'] != '' else '<no name>'
        footprint_message += f'Variant name: {variant_name}\n'
        footprint_message += f'{app.lib_obj.printLibraryStructure(ftp)}\n'
        app.footprint_footnotes.setText(footprint_message)
    else:
        device_variants = app.lib_obj.getFootprints(app.selected_device_obj)
        footprint_message = ''
        for variant in device_variants:
            dev, ftp = variant
            variant_name = dev.attrib['name'] if dev.attrib['name'] != '' else '<no name>'
            footprint_message += f'Variant name: {variant_name}\n'
            footprint_message += f'{app.lib_obj.printLibraryStructure(ftp)}\n'
        if footprint_message != '':
            app.footprint_footnotes.setText(footprint_message)
        else:
            app.footprint_footnotes.setText('Symbol only part (typically suppy symbols).')

def setSymbolFootnotes(app):
    symbol_message = ''
    for symbol in app.selected_symbol_objs:
        gate, sym = symbol
        symbol_message += f'Gate name: {gate.attrib["name"]}\n'
        symbol_message += f'{app.lib_obj.printLibraryStructure(sym)}\n'
    app.symbol_footnotes.setText(symbol_message)