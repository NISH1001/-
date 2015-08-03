#!/usr/bin/env/ python3

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


'''
    Exception class for Meaning Scraper
'''
class ScraperError(Exception):
    def __init__(self, args):
        self.args =  args

    def Display(self):
        print('ScraperError: '+''.join(self.args))



nepali_words = ['म', 'मेरो'] # nepali words in unicode
nep_eng = {} # stored as -> {nep_word: [eng_meanings]}

# first start selenium webdriver
driver = webdriver.Firefox()
driver.get("http://nirazz.blogspot.com/2014/07/roman-and-unicode-to-preeti-nepali-font.html") # our unicode to preeti site

def get_preeti(unicode_txt):
    global driver
    unicode_box = driver.find_element_by_id("unicode_text")
    unicode_box.clear()
    unicode_box.send_keys(unicode_txt)
    convert_button = driver.find_element_by_xpath("//input[@name='unicode']")
    convert_button.send_keys(Keys.RETURN)
    preeti_box = driver.find_element_by_id("legacy_text")
    return preeti_box.get_attribute('value')

def find_meanings(raw):
    splitted = raw.split(',')
    return [x.strip() for x in splitted if x != '']

for x in nepali_words:
    preeti = get_preeti(x)
    print(preeti)
    result = requests.post("http://dictionary.com.np/nepali.php",
                {'search2nep':preeti,
                'submit1':'Search'}
    )
    result_text = result.text

    soup = BeautifulSoup(result_text, "html.parser")
    result_elem = soup.findAll(attrs={'class':'font11'})

    if len(result_elem) != 4:
        continue
    # Extract the meaning, if not present, continue
    raw = result_elem[0].text
    if raw == None or raw == '':
        continue
    # in case multiple meanings are present
    nep_eng[x] = find_meanings(raw)

print(nep_eng)
driver.close()
