#!/usr/bin/python
# coding: utf-8
import re,collections
def min_nep(text): return re.sub('[ ू ी ो ौ ् ंे ृ िाैैैै ूुै]','',text)
def minWords(text): return re.sub('[a-z()]+','',text)

def searchx_in(a,b):
    result =  re.search('.*'+str(a)+'.*', str(b))
    return result is not None

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

NWORDS = train((minWords(open('data.txt').read())).split())
print (NWORDS)
def candie(word):
    return set (w for w in NWORDS if searchx_in(min_nep(word),w) and (len(w)-2)<= len(min_nep(word))<=(len(w)+2))

def best_word(word):
    return max(candie(word),key=NWORDS.get)
if __name__=='__main__':
    print (best_word('मने'))
    print (best_word('केरा'))
