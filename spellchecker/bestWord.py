import re,collections

def min_nep(text): return re.sub('[ ू ी ो ौ ् ंे ृ िाैैैै ूुै]','',text)

def minWords(text): return re.sub('[a-z()]+','',text)


def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

NWORDS = train((minWords(open('data.txt').read())).split())

def searchx_in(a,b):
    result =  re.search('.*'+str(a)+'.*', str(b))
    return result is not None
def candie(word):
    return set (w for w in NWORDS if searchx_in(min_nep(word),min_nep(w)) and (len(w)-1)<= len(word)<=(len(w)+1))
def best_word(word):
    if word in NWORDS:
        candidates=[word]
    else:
        candidates=candie(word) or [word] # candie may be empty
    return max(candidates,key=NWORDS.get)

if __name__=='__main__':
    print (candie('माने'))
    print (best_word('मने'))
    print (candie('बराल'))
