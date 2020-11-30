#!/usr/bin/python3

import tkinter as tk

def tabsField(frame, controller):
    tabs = tk.Frame(master=frame)
    tabs.pack(anchor=tk.W)
    tmpBtn = tk.Button(master=tabs, width='20', text='Documents', command=lambda: controller.show_frame('docs'))
    tmpBtn.grid(column=0, row=0, sticky=tk.W)
    tmpBtn = tk.Button(master=tabs, width='20', text='EAGLE Lib', command=lambda: controller.show_frame('eagle'))
    tmpBtn.grid(column=1, row=0, sticky=tk.W)
