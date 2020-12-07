#!/usr/bin/python3

import xml.etree.ElementTree as et
import os

from PyQt5.QtWidgets import QGraphicsScene

xml_header = '<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE eagle SYSTEM "eagle.dtd">\n'

class EagleLibrary:
    def __init__(self, path):
        self.tree = et.parse(path)
        self.root = self.tree.getroot()

    def getDevices(self, select=None):
        devices = list(self.root.iter('deviceset'))

        if select:
            try:
                devices = [device for device in devices if device.attrib['name'] == select][0]
            except:
                return []

        return devices

    def getConnections(self, device, select=None):
        connections = list(device.iter('device'))
        if select != None:
            connections = [obj for obj in connections if obj.attrib['package'] == select]
        return connections

    def getSymbols(self, device):
        symbols = []
        gates = list(device.iter('gate'))

        for gate in gates:
            symbol = [obj for obj in self.root.iter('symbol') if obj.attrib['name'] == gate.attrib['symbol']]
            if len(symbol) == 1:
                symbol = symbol[0]
                symbols.append((gate, symbol))
            else:
                return []

        return symbols

    def getFootprints(self, device, select=None):
        footprints = []
        devices = list(device.iter('device'))

        for device in devices:
            try:
                footprint = [obj for obj in self.root.iter('package') if obj.attrib['name'] == device.attrib['package']]
                if len(footprint) == 1:
                    footprint = footprint[0]
                    footprints.append((device, footprint))
                else:
                    return []
            except:
                return []

        if select:
            try:
                footprints = [tupl for tupl in footprints if tupl[1].attrib['name'] == select]
            except:
                return []

        return footprints

    def getLayers(self, number=None, name=None):
        layers = list(self.root.iter('layer'))
        if number:
            layers = [layer for layer in layers if layer.attrib['number'] == number]
        if name:
            layers = [layer for layer in layers if layer.attrib['name'] == name]

        if len(layers) == 1:
            layers = layers[0]
        return layers

    def getElement(self, element):
        elements = list(self.root.iter(element))
        return elements

    def __recurse(self, element, depth=0):
        # tmp = f'{depth:2d}: {".  " * depth}{element.tag}{("-->" + str(element.attrib)) if len(element.attrib) > 0 else ""}\n'
        tagAndText = f'{element.tag} [{element.text}]' if element.text != None and len(element.text) > 1 else f'{element.tag}'
        tmp = f'{" |  " * depth}{tagAndText}{(" -->  " + str(element.attrib)) if len(element.attrib) > 0 else ""}\n'
        self.__printMessage += tmp
        children = list(element)
        for child in children:
            self.__recurse(child, depth+1)

    def printLibraryStructure(self, element=None):
        self.__printMessage = ''
        if element == None:
            self.__recurse(self.root)
        else:
            self.__recurse(element)
        return self.__printMessage

    def exportLibrary(self, filename):
        with open(filename, 'w') as f:
            f.write(xml_header)
        self.tree.write(open(filename, 'ab'), encoding='UTF-8')
