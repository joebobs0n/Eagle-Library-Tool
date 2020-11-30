#!/usr/bin/python3

import tkinter as tk
from tkinter import font as tkfont
from src.pages.docs import docs
from src.pages.eagle import eagle


class EagleToolApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight='bold')
        self.body_font = tkfont.Font(family='Helvetica', size=12, weight='bold')

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for frame in [docs, eagle]:
            page_name = frame.__name__
            frame = frame(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame('docs')

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def load_library(self, path):
        pass
