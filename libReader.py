#!/usr/bin/python3

import libExtractor as le
import tkinter as tk
from tkinter import font as tkfont
from tkinter import filedialog
import os
import xml.etree.ElementTree as et


class EagleReader(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight='bold')
        self.body_font = tkfont.Font(family='Helvetica', size=12, weight='bold')

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for idx, F in enumerate((docs, eagle)):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame('docs')

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


def tabsField(self, controller):
    tabs = tk.Frame(master=self)
    tabs.pack(anchor=tk.W)
    tmpBtn = tk.Button(master=tabs, width='20', text='Documents', command=lambda: controller.show_frame('docs'))
    tmpBtn.grid(column=0, row=0, sticky=tk.W)
    tmpBtn = tk.Button(master=tabs, width='20', text='EAGLE Lib', command=lambda: controller.show_frame('eagle'))
    tmpBtn.grid(column=1, row=0, sticky=tk.W)


class docs(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tabsField(self, controller)

        self.title = tk.Label(self, text='Documents Page', font=controller.title_font, pady=20)
        self.title.pack()

        self.file_label = tk.Label(self, text='Select Eagle Library', font=controller.body_font, foreground='red')
        self.file_label.pack()

        self.explore_button = tk.Button(self, text='Browse', command=self.browseFiles)
        self.explore_button.pack()

    def browseFiles(self):
        filename = filedialog.askopenfilename(initialdir=os.getcwd(), title='Select Eagle Library', filetypes=(("lbr files","*.lbr"),("all files","*.*")))
        _, ext = os.path.splitext(filename)
        if ext == '.lbr':
            self.file_label.configure(text=f'File Opened <{filename}>', foreground='green')
            eagleFrame = self.controller.frames['eagle']
            eagleFrame.extractData(filename)
        else:
            self.file_label.configure(text=f'The file <{filename}> is not a valid library.', foreground='red')


class eagle(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tabsField(self, controller)

        self.title = tk.Label(self, text='Eagle Library Reader Page', font=controller.title_font, pady=20)
        self.title.pack()

        self.status_label = tk.Label(self, text='No Library Loaded', font=controller.body_font, foreground='red')
        self.status_label.pack()

        self.data_frame = tk.Frame(self, padx=5, pady=5)
        self.data_frame.pack()

        self.devices_label = tk.Label(master=self.data_frame, text='Devices:', font=controller.body_font)
        self.devices_label.grid(column=0, row=0, sticky=tk.W)
        self.devices_listbox = tk.Listbox(master=self.data_frame, width=25, height=44, selectmode=tk.SINGLE)
        self.devices_listbox.bind('<<ListboxSelect>>', self.deviceSelect)
        self.devices_listbox.grid(column=0, row=1)

        self.spacer1 = tk.Canvas(master=self.data_frame, width=5)
        self.spacer1.grid(column=1, row=1)

        self.footprint_label = tk.Label(master=self.data_frame, text='Footprint:', font=controller.body_font)
        self.footprint_label.grid(column=2, row=0, sticky=tk.W)
        self.footprint_canvas = tk.Canvas(master=self.data_frame, width=800, height=800, background='#1f1f1f')
        self.footprint_canvas.grid(column=2, row=1)

        self.spacer2 = tk.Canvas(master=self.data_frame, width=5)
        self.spacer2.grid(column=3, row=1)

        self.symbol_label = tk.Label(master=self.data_frame, text='Symbol:', font=controller.body_font)
        self.symbol_label.grid(column=4, row=0, sticky=tk.W)
        self.symbol_canvas = tk.Canvas(master=self.data_frame, width=800, height=800, background='#1f1f1f')
        self.symbol_canvas.grid(column=4, row=1)

        self.notes_label = tk.Label(self, text='Notes:', padx=20)
        self.notes_label.pack(anchor=tk.W)

    def deviceSelect(self, evt):
        currentDevice = self.devices_listbox.get(self.devices_listbox.curselection())
        self.status_label.configure(text=f'{currentDevice}')

        ## STOPPED HERE

    def extractData(self, filename):
        self.filename = filename
        self.layers, self.footprints, self.symbols, self.devices = le.parseLibrary(self.filename)
        self.status_label.configure(text=f'Library Read Successfully', foreground='green')
        self.updateSelection()

    def updateSelection(self):
        self.devices_listbox.delete(0, tk.END)
        for device in self.devices:
            self.devices_listbox.insert(tk.END, device.attribs['name'])



if __name__ == '__main__':
    app = EagleReader()
    app.title('EAGLE Library Reader')
    app.mainloop()

    exit()
