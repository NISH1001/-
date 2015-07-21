#!/usr/bin/env/ python3

import requests
from bs4 import BeautifulSoup


'''
    Exception class for Meaning Scraper
'''
class ScraperError(Exception):
    def __init__(self, args):
        self.args =  args

    def Display(self):
        print('ScraperError: '+''.join(self.args))


''' 
    class MeaningScraper:
        We pass in the nepali word and it outputs
        corresponding meaning if found.

    METHODS:

'''

class NepaliToEnglish(object):
    def __init__(self, main_url, preeti_required=False):
        # the url where we seek the meaning
        self.url = main_url     
        # if the site requires preeti font
        self.preeti_required = preeti_required
        self.preeti_converter_url = None

    def SetPreetiConverterUrl(self, url):
        self.preeti_converter_url = url

    def GetEngWord(self, nep_unicode):
        if self.preeti_required:
            nep_word = self.GetPreeti(nep_unicode)
        else:
            nep_word = nep_unicode

        meaning = self.ScrapEnglishWord(nep_word)
        return meaning

    def GetPreeti(self, unicode_str):
        if self.preeti_converter_url is None:
            raise ScraperError("Preeti Converter Url not set!!")

        post_data = {
            'userInput' : unicode_str
        }
        response = requests.post(self.preeti_converter_url, post_data)
        response_text = response.text

        soup = BeautifulSoup(response_text, "html.parser")
        # get the preeti equivalent to feed
        try:
            result_objects = soup.find_all("textarea")
            for x in result_objects:
                if x.attrs['name'] == "output":
                    return x.text
            raise Exception
        except Exception:
            raise ScraperError('Problem with finding the Preeti equivalent')

    def ScrapEnglishWord(self, nepali_word):
        post_data = {
            'search2nep' : nepali_word
        }
        response = requests.post(self.url, post_data)
        resonse_text = response.text

        soup = BeautifulSoup(resonse_text, "html.parser")
        try:
            result_objects = soup.find_all('font')
            # iterate it, the first with class font11 is result
            for x in result_objects:
                if x.has_key('class') and 'font11' in x.attrs['class']:
                    return x.text
            raise Exception
        except Exception:
            raise ScraperError('Problem finding the english equivalent of the preeti font Entered')

