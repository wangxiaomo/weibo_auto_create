#-*- coding: utf-8 -*-

class Writer(object):
    def __init__(self, filename):
        self.hdl = open(filename, 'w')

    def __del__(self):
        self.hdl.close()

    def append(self, text):
        self.hdl.write(text + "\n")

class Reader(object):
    def __init__(self, filename):
        self.hdl = open(filename, 'r')

    def __del__(self):
        self.hdl.close()

    def read(self):
        return self.readline()
