#!/usr/bin/python3

import tkinter as tk
import src.pages.helpers as hlp
import numpy as np
import src.lbrHandler as lh

class eagle(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        hlp.tabsField(self, controller)
        self.dimension = 500
        self.viewer_center = (self.dimension/2, self.dimension/2)

# HEADER
        # PAGE TITLE
        tk.Label(self, text='Eagle Library Reader Page', font=controller.title_font, pady=20).pack()
        # STATUS LABEL
        self.status_label = tk.Label(self, text='No Library Loaded', font=controller.body_font, foreground='red')
        self.status_label.pack()
        # DATA FRAME
        self.data_frame = tk.Frame(self, padx=5, pady=5)
        self.data_frame.pack()

# DEVICE SELECTION
        # LABEL
        tk.Label(master=self.data_frame, text='Device Select:', font=controller.body_font).grid(column=0, row=0, sticky=tk.W)
        # LISTBOX
        self.devices_listbox = tk.Listbox(master=self.data_frame, width=20, selectmode=tk.SINGLE)
        self.devices_listbox.bind('<<ListboxSelect>>', self.deviceSelect)
        self.devices_listbox.grid(column=0, row=1, sticky='ns')
        # SCROLLBAR
        self.devices_scrollbar = tk.Scrollbar(master=self.data_frame)
        self.devices_scrollbar.grid(column=1, row=1, sticky='ns')
        # ATTACH SCROLLBAR TO LISTBOX
        self.devices_listbox.config(yscrollcommand=self.devices_scrollbar.set)
        self.devices_scrollbar.config(command=self.devices_listbox.yview)

# FOOTPRINT SELECTION
        # LABEL
        tk.Label(master=self.data_frame, text='Footprint Select:', font=controller.body_font).grid(column=2, row=0, sticky=tk.W)
        # LISTBOX
        self.footprints_listbox = tk.Listbox(master=self.data_frame, width=20, selectmode=tk.SINGLE)
        self.footprints_listbox.bind('<<ListboxSelect>>', self.footprintSelect)
        self.footprints_listbox.grid(column=2, row=1, sticky='ns')
        # SCROLLBAR
        self.footprints_scrollbar = tk.Scrollbar(master=self.data_frame)
        self.footprints_scrollbar.grid(column=3, row=1, sticky='ns')
        # ATTACH SCROLLBAR TO LISTBOX
        self.footprints_listbox.config(yscrollcommand=self.footprints_scrollbar.set)
        self.footprints_scrollbar.config(command=self.footprints_listbox.yview)

# FOOTPRINT VIEWER
        # LABEL
        tk.Label(master=self.data_frame, text='Footprint View:', font=controller.body_font).grid(column=4, row=0, sticky=tk.W)
        # CANVAS
        self.footprint_canvas = tk.Canvas(master=self.data_frame, width=self.dimension, height=self.dimension, background='#1f1f1f')
        self.footprint_canvas.grid(column=4, row=1)
        self.initCanvas(self.footprint_canvas)

# SYMBOL VIEWER
        # LABEL
        tk.Label(master=self.data_frame, text='Symbol View:', font=controller.body_font).grid(column=5, row=0, sticky=tk.W)
        # CANVAS
        self.symbol_canvas = tk.Canvas(master=self.data_frame, width=self.dimension, height=self.dimension, background='#1f1f1f')
        self.symbol_canvas.grid(column=5, row=1)
        self.initCanvas(self.symbol_canvas)

# NOTES
        # LABEL
        self.notes_label = tk.Label(self, text='Notes:', padx=10, pady=10)
        self.notes_label.pack(anchor=tk.W)

    def initCanvas(self, canvas):
        canvas.create_line(self.dimension/2, self.dimension/2-10, self.dimension/2, self.dimension/2+10, fill='white', width='2')
        canvas.create_line(self.dimension/2-10, self.dimension/2, self.dimension/2+10, self.dimension/2, fill='white', width='2')

        for x in np.linspace(10, self.dimension-10, round(self.dimension/10-1)):
            for y in np.linspace(10, self.dimension-10, round(self.dimension/10-1)):
                canvas.create_oval(x-1, y-1, x+1, y+1, fill='white')

    def resetCanvas(self, canvas):
        canvas.delete('all')
        self.initCanvas(canvas)

    def loadLibrary(self, filename):
        self.filename = filename
        self.library_obj = lh.EagleLibrary(self.filename)
        self.status_label.configure(text=f'Library Read Successfully', foreground='green')
        self.updateDeviceSelection()

    def deviceSelect(self, evt):
        deviceName = self.devices_listbox.get(self.devices_listbox.curselection())
        self.status_label.configure(text=f'{deviceName}')
        self.currentDevice = [obj for obj in self.devices if obj.attrib['name'] == deviceName][0]
        self.updateFootprintSelection()

    def footprintSelect(self, evt):
        footprintName = self.footprints_listbox.get(self.footprints_listbox.curselection())
        self.currentFootprint = [obj for obj in self.footprints if obj.attrib['name'] == footprintName][0]
        self.resetCanvas(self.footprint_canvas)
        self.footprint_canvas.create_text(self.viewer_center, text=footprintName, font=self.controller.body_font, fill='red')

    def updateDeviceSelection(self):
        self.devices = self.library_obj.getDevices()
        self.devices_listbox.delete(0, tk.END)
        for device in self.devices:
            self.devices_listbox.insert(tk.END, device.attrib['name'])

    def updateFootprintSelection(self):
        self.footprints = self.library_obj.getFootprints(self.currentDevice)
        self.footprints_listbox.delete(0, tk.END)
        for footprint in self.footprints:
            self.footprints_listbox.insert(tk.END, footprint.attrib['name'] if footprint.attrib['name'] != '' else '<no name>')