#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import re, os


"""
a helper function to check folder existence
"""
def FolderExist(folderpath):
    if not os.path.exists(folderpath):
        return False
    else: return True

"""
our Manual Exception class
"""
class ManualError(Exception):
    def __init__(self, args):
        self.args = args

    def Display(self):
        print(''.join(self.args))

"""
Setopati class:
accepts a url
Methods:
    Get:         get request to setopati's desired url
    Extract:     Abstract news extract methods -> real scraping happens here
                 returns string bytes with utf-8

"""
class Setopati(object):
    def __init__(self, url):
        self.url = url
        self.result = None

    def Get(self):
        # headers is required for simulating that this get request is from a browser
        self.result = requests.get(self.url, headers = {'User-Agent' : 'Mozilla/5.0'} )
        #self.result = requests.get(self.url)
        return self.result

    def Extract(self):
        try:
            # if no OK
            if self.result.status_code != 200:
                raise ManualError("the request is not OK")

            else:
                # beautifulsoup root extractor
                extractor = BeautifulSoup(self.result.content, "html.parser")
                newsbox = extractor.find("div", {'id' : 'newsbox'} )
                news = newsbox.find_all(["div", "p"])

                news_total = bytes('', 'UTF-8')

                for div in news:
                    text = div.get_text()
                    text = text.strip()
                    if text[0:6] == "window":
                        continue
                    news_total += bytes(text+'\n', 'UTF-8')
                return news_total

        except ManualError as merr:
            merr.Display()
            return ''
        

def main():
    setopatiurl = "http://setopati.com/bichar/"
    folderpath = "setopati"

    if not FolderExist(folderpath):
        print("folder doesnot exist; hence making it...")
        os.makedirs(folderpath)

    for i in range(500,4000):
        print("have patience while scraping .... {}".format(i))
        setopati = Setopati(setopatiurl + str(i) )
        setopati.Get()
        path = folderpath + "/" + str(i)
        extracted_text = setopati.Extract()
        if not extracted_text:
            print("skipping... {}".format(i))
            continue
        outfile = open(path, "wb")
        outfile.write(extracted_text)
        outfile.close()


if __name__=="__main__":
    main()

