#!/usr/bin/env python3

import json     # might not be used
import goslate
import requests
import sqlite3
from bs4 import BeautifulSoup


'''
    Exception class for Dictionary Generator
'''
class DictGenException(Exception):
    def __init__(self, args):
        self.args = args

    def Display(self):
        print('DictGenError: '+''.join(self.args))


''' 
    class DictionaryGenerator:
        We feed in the nepali words/phrases and it 
        will generate a database with nepali words 
        and corresponding english words.

    METHODS:
    * FromGoogleTranaslate:     
            We use the google Translate's API goslate. !! well we won't be using that now

    * FromOnlineWebsite:
            We use the online nepali to english dictionary.
            From the website "http://dictionary.com.np/nepali.php"
            Use POST methods and other if necessary.
'''
    
class DictionaryGenerator(object):
    def __init__(self, nep_words_list):
        self.nep_words = nep_words_list
        self.nep_eng   = {}

    def LoadNepaliWords(self):
        
