#!/usr/bin/env/ python3

import requests
from bs4 import BeautifulSoup
from NepaliToEnglish import ScraperError
import re, json


'''
    class ExtractVocab:
        extract nep-english vocab from
        http://www.dicts.info/vocabulary/?l1=nepali

    METHODS:
        * GetPairs      : Loads the nep-eng pairs into pairs attribute
                         ofthe class. gets the main website and iterates 
                         through every category found in the page
        *ExtractFrom    : Does the real extraction of word pairs. called by 
                        GetPairs() method which extracts pairs from spacific
                        link passed to it.

'''

class ExtractVocab(object):
    def __init__(self):
        self.url = "http://www.dicts.info/vocabulary/"
        self.pairs = {}

    def GetPairs(self):
        response = requests.get(self.url+"?l1=nepali")
        response_text = response.text

        soup = BeautifulSoup(response_text, "html.parser")
        links = soup.find_all('a')

        for link in links: # visit all the useful links
            # each link we need has '?group=<something>' in href
            if 'group' in link.attrs['href']:
                self.ExtractFrom(link.attrs['href'])
        
        # Now that the pairs are extracted, we save them to vocab.txt
        f = open('vocab.txt', "w")
        f.write(json.dumps(self.pairs, ensure_ascii=False))


    def ExtractFrom(self, link):

        response = requests.get(self.url+link)
        if response.status_code != 200:
            raise ScraperError("Bad response from the server")

        response_text = response.text

        soup = BeautifulSoup(response_text, "html.parser")
        tds = soup.find_all('td') # Results are in table cells

        try:
            for x in tds:
                if len(x.find_all('b')) !=0: # english word is in bold letters
                    wordpairs = x.text.split('\n') # wordpairs in single td
                    wordpairs = [a for a in wordpairs if a!=''] # remove empty
                    for pair in wordpairs:
                        eng = pair.split()[0]
                        nep = re.split('[a-zA-Z]+', pair)[1] # first is empty, so discard
                        nep = nep.split(',')
                        for each in nep:
                            if not each == '':
                                self.pairs[each] = eng
        except Exception:
            raiseScraperError("Error while extracting nep-eng pairs")
                        
