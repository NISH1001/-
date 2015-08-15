#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import re

url = "http://www.bdword.com/search.php"

class TranslateError(Exception):
    def __init__(self, args):
        self.args = args

    def display(self):
        print(''.join(self.args))

def check_verb(nep):
    return bool( re.search("(र्नु)|(उनु)|(न्नु)|(नु)", nep))

"""
returns a dict of keys : 'verb', 'non-verb'

- feed any english word 
- scraps out all the possible nepali translation words
- checks if the nepali word is a verb

final result:
    {
        'verb' : certain list
        'non-verb' : certain list
    }

now from our existing english dictionary database
we can feed those english words and we can now create a new database
the new database may onlny be of verb or all the nepali synonym word
"""
def EnglishToNepali(eng):
    query = {'q' : eng, 'lang' : 'nepali'}
    response = requests.post(url, params=query)

    try:
        if response.status_code!=200:
            raise TranslateError("effin response<>200 :D")
        else:
            extractor = BeautifulSoup(response.content, "html.parser")
            translated = extractor.find("div", {'class': "bs-callout bs-callout-danger"})

            translated_text = translated.get_text().strip().split("\n")[-1].strip()
            splitted = translated_text.split(':')
            list_nep = splitted[1].split(',')
            list_nep = [ nep.strip() for nep in list_nep ]

            #list_verb = [ nep for nep in list_nep if check_verb(nep) ]
            #list_non_verb = [ nep for nep in list_nep if nep not in list_verb ]
            list_verb = []
            list_non_verb = []

            for nep in list_nep:
                if check_verb(nep):
                    list_verb.append(nep)
                else:
                    list_non_verb.append(nep)

            res = {'verb' : list_verb, 'non-verb' : list_non_verb}
            return res

    except TranslateError as terr:
        terr.display()
        return {}

def main():
    eng = str(input("enter english word : "))
    nep = EnglishToNepali(eng)
    print(nep)

if __name__=="__main__":
    main()

