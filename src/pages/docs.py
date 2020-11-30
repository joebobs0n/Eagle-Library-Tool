#!/usr/bin/python3

import os
import tkinter as tk
import src.pages.helpers as hlp
from tkinter import filedialog as browser

class docs(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        hlp.tabsField(self, controller)

        self.title = tk.Label(self, text='Documents Page', font=controller.title_font, pady=20)
        self.title.pack()

        self.file_label = tk.Label(self, text='Select Eagle Library', font=controller.body_font, foreground='red')
        self.file_label.pack()

        self.explore_button = tk.Button(self, text='Browse', command=self.browseFiles)
        self.explore_button.pack()

    def browseFiles(self):
        filename = browser.askopenfilename(initialdir=os.getcwd(), title='Select Eagle Library', filetypes=(("lbr files","*.lbr"),("all files","*.*")))
        _, ext = os.path.splitext(filename)
        if ext == '.lbr':
            self.file_label.configure(text=f'File Opened <{filename}>', foreground='green')
            eagleFrame = self.controller.frames['eagle']
            eagleFrame.loadLibrary(filename)
        else:
            self.file_label.configure(text=f'The file <{filename}> is not a valid library.', foreground='red')
