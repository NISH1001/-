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
BIGRAM= train([''.join(text[x:x+2]) for x in range(len(text)-1)])

#bigrams=[text[x:x+2] for x in range(len(text)-1)]
#print(BIGRAM)
NWORDS = train(text)

# change a word to pure string of  nepali alphabets only
def min_nep(text): return re.sub('[ ू ी ो ौ ् ंे ृ िाैैैै ूुै]','',text)

def searchx_in(a,b):
    result =  re.search('.*'+str(a)+'.*', str(b))
    return result is not None

# give set of best candidates for given words
def candie(word):
    return set (w for w in NWORDS if searchx_in(min_nep(word),min_nep(w)) and (len(w)-1)<= len(word)<=(len(w)+1))

def bi_word(prev_word,candie_word):
    x=set(''.join([prev_word,word]) for word in candie_word)
    y=[]
    for a in x:
        if a in BIGRAM:
            y.append(a)
    b=max(y,key=BIGRAM.get)
    for word in candie_word:
        if searchx_in(word,b):
            return [word,BIGRAM[word]]

def best_word(word):
    if word in NWORDS:
        candidates=[word]
    else:
        candidates=candie(word) or [word]
    b=max(candidates,key=NWORDS.get)
    #return (max(candidates,key=NWORDS.get),NWORDS[max(candidates,key=NWORDS.get)])
    return [b,NWORDS[b]]

def correct(prev,word):
    a=bi_word(prev,candie(word))
    b=best_word(word)
    if a[0] is b[0]:
        return a[0]
    elif a[1]*8>b[1]:
        return a[0]
    else:
        return b[0]

if __name__=='__main__':
#    print(candie('पनि'))
    print (bi_word('प्रयोग',candie('पानि')))
#    print (candie('माने'))
#    print (best_word('मने'))
    print(best_word('पानि'))
#    print (candie('बराल'))
    print (correct('प्रयोग','पानि'))

