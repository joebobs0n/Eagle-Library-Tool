#!/bin/usr/python3

def dump(obj):
    for attr in dir(obj):
        print(f'obj.{attr} = {getattr(obj, attr)}')