#!/usr/bin/env python3

import re
import codecs
import time
from collections import defaultdict, OrderedDict
import pickle
import operator

try:
    from .ngramdb import NgramDB
    from .ngram_mem import NgramMem
except:
    from ngramdb import NgramDB
    from ngram_mem import NgramMem

"""
Ngram class: 
-- For now we use upto quadgrams
-- uses our ngram database handler ngramdb 
-- sqlite database is used

attributes:
    bigrams,trigrams,quadgrams are all dictionary with key as tuple of words
    eg: bigrams[('happy', 'man)] = somecount

functions:
    count()                         : get the occurence count of the ngrams sequence
    probability()                   : get the probability of count -> count/total
    __generate_probability_table    : private function to generate our probablity table (uses bigrams)
    generate_sentence               : get the final sentence using the probability table
"""
class Ngram(object):

    def __init__(self, data_path="../data/ngrams/", load_type="memory"):
        self.load_type = load_type
        self.unigrams = OrderedDict()
        self.bigrams  = OrderedDict()
        self.trigrams = OrderedDict()
        self.quadgrams = OrderedDict()

        # this is ngrams database handler
        self.ngramdb = NgramDB(data_path+"ngrams.db")
        #self.ngramdb.create_table_all()
        if load_type=="memory":
            ngram_mem = NgramMem(data_path=data_path)
            ngram_mem.load_all(pickle=True)
            self.__count = ngram_mem.count
        else:
            self.__count = self.ngramdb.count

    def close_ngramdb(self):
        self.ngramdb.close()

    """
    get integer count of the sequence of words
    seq : is a tuple of words
    returns count of occurences of such sequence
    if total count is needed just set total to True
        and pass garbage seq
    """
    def count(self, seq, total=False):
        return self.__count(seq, total)

    """ get probability of the ngram sequence"""
    def probability(self, seq):
        length = len(seq)
        count = self.count(seq, total=False)
        total = self.count(seq, total=True)
        if not count or not total:
            return 0.0
        else:
            return count/total
    
    """ private function: create our 2d table with probability using list comprehension"""
    def __generate_probability_table(self, seq):
        n = len(seq)
        table = [ 
                    [
                        -1.0
                        if x==y else 1*self.probability( tuple([ seq[x],seq[y] ]) ) 
                        for y in range(n)
                    ] 
                for x in range(n) 
            ]
        return table

    """ generate the first phase sentence
    """
    def generate_sentence(self, seq):
        n = len(seq)
        table = self.__generate_probability_table(seq) # get the table

        # track the row index in the table
        index_row = 0

        # resultant list
        res = [seq[0]]

        # main generator
        for i in range(n-1):
            # get the word with max probablity ie word(x+1) that is likley to occur after the world(x)
            index_col, max_prob = max(enumerate(table[index_row]), key=lambda x: x[1])

            res.append(seq[index_col])
            #table[index_col] = [0.0]*n
            # set the column prob negative -> no need of previous words for upcoming words
            for i in range(n):
                table[i][index_row] = -1

            # new index row 
            index_row = index_col
        return res


def main():
    start = time.time()
    ngram = Ngram(data_path="../data/ngrams/", load_type="memory")
    print("time : ",time.time() - start)

    # just a ngram tester
    while True:
        seq = str(input("enter sequence of words: "))
        if not seq:
            continue
        if seq=="exit":
            break
        seq = tuple(seq.split())
        sentence = ngram.generate_sentence(seq)
        print(sentence)

    ngram.close_ngramdb()

if __name__=="__main__":
    main()




