#!/usr/bin/env python3

'''
    THIS MODULE CREATES THE DATABASE FROM THE RAW DATA
    SCRAPED
'''


'''
    Exception class for Dictionary Generator
'''
class DictGenException(Exception):
    def __init__(self, args):
        self.args = args

    def Display(self):
        print('DictGenError: '+''.join(self.args))



