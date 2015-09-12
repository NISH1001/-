import re,collections

class SpellCorrectorError(Exception):
    def __init__(self,args):
        self.args=args
    def Display(self):
        print("Spell-Corrector error:"+ ''.join(self.args))

# remove any english characters for the text
def minWords(text): return re.sub('[a-z()१२३४५६७८९०‘।.!/]+','',text)

# trains ;) from given 'data.txt' file
# and stores words in NWORDS
def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model
text=(minWords(open('data.txt').read())).split()
bigrams=[text[x:x+2] for x in range(len(text)-1)]
#print(bigrams)
NWORDS = train(text)

# change a word to pure string of  nepali alphabets only
def min_nep(text): return re.sub('[ ू ी ो ौ ् ंे ृ िाैैैै ूुै]','',text)

def searchx_in(a,b):
    result =  re.search('.*'+str(a)+'.*', str(b))
    return result is not None

# give set of best candidates for given words
def candie(word):
    return set (w for w in NWORDS if searchx_in(min_nep(word),min_nep(w)) and (len(w)-1)<= len(word)<=(len(w)+1))

def bi_word(word1,word2):
    pass

def best_word(word):
    if word in NWORDS:
        candidates=[word]
    else:
        candidates=candie(word) or [word]
    return max(candidates,key=NWORDS.get)

if __name__=='__main__':
    print (candie('माने'))
    print (best_word('मने'))
    print (candie('बराल'))
