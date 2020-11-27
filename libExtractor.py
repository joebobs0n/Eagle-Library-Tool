#!/usr/bin/python3

import xml.etree.ElementTree as et

libPath = 'ElegooMarsHeater.lbr'

desiredItems = ['layers', 'packages', 'symbols', 'devicesets']


class Object:
    def __init__(self, name, attribs):
        self.name = name
        self.attribs = attribs
        self.children = []
        self.hasChildren = False

    def addChild(self, object):
        self.hasChildren = True
        self.children.append(object)


def buildTree(element):
    children = list(element)
    thisObj = Object(element.tag, element.attrib)

    for child in children:
        thisObj.addChild(buildTree(child))

    return thisObj


def parseLibrary(path):
    tree = et.parse(path)
    root = tree.getroot()

    objectsList = []

    desiredRoots = [list(root.iter(item))[0] for item in desiredItems]
    for element in desiredRoots:
        objectsList.append(buildTree(element))

    layers = objectsList[0].children
    footprints = objectsList[1].children
    symbols = objectsList[2].children
    devices = objectsList[3].children

    return layers, footprints, symbols, devices


if __name__ == '__main__':
    layers, footprints, symbols, devices = parseLibrary(libPath)

    print('-- Object Lists '.ljust(25, '-'))
    print('  # layers:'.ljust(19, ' ') + f'{len(layers):4d}')
    print('  # footprints:'.ljust(19, ' ') + f'{len(footprints):4d}')
    print('  # symbols:'.ljust(19, ' ') + f'{len(symbols):4d}')
    print('  # devices:'.ljust(19, ' ') + f'{len(devices):4d}')

    exit()