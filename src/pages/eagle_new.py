#!/usr/bin/python3

import tkinter as tk
import src.pages.helpers as hlp
import src.lbrHandler as lh


class viewer:
    dims = (500, 500)
    center = (250, 250)

class eagle(tk.Frame):
    def __init__(self, parent, controller, viewer_dimensions=None):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        hlp.tabsField(self, controller)
        if viewer_dimensions != None:
            viewer.dims = viewer_dimensions
            viewer.center = (viewer_dimensions[0]/2, viewer_dimensions[1]/2)


