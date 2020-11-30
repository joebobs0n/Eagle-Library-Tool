#!/usr/bin/python3

import xml.etree.ElementTree as et
import os

class EagleLibrary:
    def __init__(self, path):
        tree = et.parse(path)
        self.root = tree.getroot()

    def getDevices(self, select=None):
        devices = list(self.root.iter('deviceset'))

        if select:
            try:
                devices = [device for device in devices if device.attrib['name'] == select][0]
            except:
                return None

        return devices

    def getSymbols(self, device):
        symbols = []
        gates = list(device.iter('gate'))

        for gate in gates:
            symbol = [obj for obj in self.root.iter('symbol') if obj.attrib['name'] == gate.attrib['symbol']]
            if len(symbol) == 1:
                symbol = symbol[0]
                symbols.append((gate, symbol))
            else:
                return None

        return symbols

    def getFootprints(self, device, select=None):
        footprints = []
        devices = list(device.iter('device'))

        for device in devices:
            footprint = [obj for obj in self.root.iter('package') if obj.attrib['name'] == device.attrib['package']]
            if len(footprint) == 1:
                footprint = footprint[0]
                footprints.append((device, footprint))
            else:
                return None

        if select:
            try:
                footprints = [tupl for tupl in footprints if tupl[1].attrib['name'] == select][0]
            except:
                return None

        return footprints

    def getLayers(self):
        layers = list(self.root.iter('layer'))
        return layers

    def __recurse(self, element, depth=0):
        print(f'{depth:2d}: {".  " * depth}{element.tag}{("-->" + str(element.attrib)) if len(element.attrib) > 0 else ""}')
        children = list(element)
        for child in children:
            self.__recurse(child, depth+1)

    def printLibraryStructure(self, element=None):
        if element == None:
            self.__recurse(self.root)
        else:
            self.__recurse(element)


def printMenu():
    os.system('cls' if os.name == 'nt' else 'clear')
    options = [
        'Print whole library contents',
        'Get all devices',
        'Get single device (LM324)',
        'Get symbols from chosen device (LM324)',
        'Get all footprints for chosen device (TAC_SWITCH)',
        'Get chosen footprint (TACTILE-PTH) for chosen device (TAC_SWITCH)',
        'Get layers',
        'Exit'
    ]
    print(''.ljust(100, '-'))
    print('Eagle Library Handler (XML) Demonstrations'.center(100))
    print(''.ljust(100, '-'))
    for idx, option in enumerate(options, start=1):
        print(f'   {idx}: {option}')

if __name__ == '__main__':
    mylbr = 'testLib.lbr'
    lbr_obj = EagleLibrary(mylbr)

    while(1):
        printMenu()
        userChoice = input('User input:')
        print()

        if userChoice == '1':
            # PRINTOUT WHOLE LIBRARY XML
            lbr_obj.printLibraryStructure()

        elif userChoice == '2':
            # TEST GETTING ALL DEVICES
            devices = lbr_obj.getDevices()
            print(''.ljust(100, '-'))
            for device in devices:
                lbr_obj.printLibraryStructure(device)
                print(''.ljust(100, '-'))
            print(f'Total Devices: {len(devices):3d}')

        elif userChoice == '3':
            # TEST GETTING ONE CHOSEN DEVICE
            device = lbr_obj.getDevices('LM324')
            lbr_obj.printLibraryStructure(device)

        elif userChoice == '4':
            # TEST GETTING SYMBOLS FROM CHOSEN DEVICE
            device = lbr_obj.getDevices('LM324')
            symbols = lbr_obj.getSymbols(device)
            print(''.ljust(100, '-'))
            for symbol in symbols:
                thisgate, thissymbol = symbol
                lbr_obj.printLibraryStructure(thisgate)
                print()
                lbr_obj.printLibraryStructure(thissymbol)
                print(''.ljust(100, '-'))
            print(f'Total Symbols for {device.attrib["name"]}: {len(symbols):3d}')

        elif userChoice == '5':
            # TEST GETTING ALL FOOTPRINTS FOR CHOSEN DEVICE
            devices = lbr_obj.getDevices('TAC_SWITCH')
            footprints = lbr_obj.getFootprints(devices)
            print(''.ljust(100, '-'))
            for footprint in footprints:
                thisdevice, thisfootprint = footprint
                lbr_obj.printLibraryStructure(thisdevice)
                print()
                lbr_obj.printLibraryStructure(thisfootprint)
                print(''.ljust(100, '-'))
            print(f'Total Footprints for {devices.attrib["name"]}: {len(footprints):3d}')

        elif userChoice == '6':
            # TEST GETTING ONE FOOTPRINT FOR CHOSEN DEVICE AND PACKAGE
            devices = lbr_obj.getDevices('TAC_SWITCH')
            footprint = lbr_obj.getFootprints(devices, 'TACTILE-PTH')
            thisdevice, thisfootprint = footprint
            lbr_obj.printLibraryStructure(thisdevice)
            print()
            lbr_obj.printLibraryStructure(thisfootprint)

        elif userChoice == '7':
            # TEST GETTING LAYERS
            layers = lbr_obj.getLayers()
            for layer in layers:
                lbr_obj.printLibraryStructure(layer)

        elif userChoice == '8':
            exit()

        else:
            print('Bad selection...')

        input('\nPress ENTER to continue...')
