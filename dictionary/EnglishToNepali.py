#!/usr/bin/env/ python3

import requests
from bs4 import BeautifulSoup
from NepaliToEnglish import ScraperError
import re, json


'''
here we feed in the english words (verbs actually)
and we get the preeti output, which will later be converted
to unicode
'''

# website used is http://dictionary.com.np
def get_nepali_meaning(word):
    url = 'http://dictionary.com.np'
    response = requests.post(url,
                {'search2nep': word,
                    'submit1' : 'Search'})

    soup = BeautifulSoup(response.content, 'html.parser')

    result = soup.find('font', 'nepfont').get_text()
    return result
