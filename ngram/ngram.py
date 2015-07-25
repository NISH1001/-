#!/usr/bin/env python3

import re
import codecs
import time
from collections import defaultdict
import pickle

"""
Ngram class: 
-- For now we we upto trigrams

attributes:
    bigrams,trigrams are all dictionary with key as tuple of words
    eg: bigrams[('happy', 'man)] = somecount
"""
class Ngram(object):

    def __init__(self):
        self.unigrams = {}
        self.bigrams  = {}
        self.trigrams = {}

    # load all the ngrams dict from text files
    def load_all(self, pickle=False):
        self.load_bigrams(file_ngrams="ngramdata/2grams.txt")
        self.load_trigrams(file_ngrams="ngramdata/3grams.txt")

    # load the bigrams from the desired file
    def load_bigrams(self, file_ngrams = "ngramdata/2grams.txt"):
        print(file_ngrams)

        # codecs is used to remove conflicts with encoding schemes
        with codecs.open(file_ngrams, 'rb', encoding='utf-8', errors='ignore' ) as f:
            print("loading bigrams... from {}".format(file_ngrams))
            for line in f:
                splitted = line.split()
                self.bigrams[ (splitted[1], splitted[2]) ] = splitted[0]
        print("bigrams loaded successfully... :P")

    # load the trigrams
    def load_trigrams(self, file_ngrams = "ngramdata/3grams.txt"):
        # codecs is used to remove conflicts with encoding schemes
        with codecs.open(file_ngrams, 'rb', encoding='utf-8', errors='ignore' ) as f:
            print("loading trigrams... from {}".format(file_ngrams))
            for line in f:
                splitted = line.split()
                self.trigrams[ (splitted[1], splitted[2], splitted[3]) ] = splitted[0]
        print("trigrams loaded successfully... :P")

    # general ngrams loader from pickle file
    def load_ngrams_pickle(self, pickle_file = "ngramdata/2grams.ng", n=2):
        print("loading pickle... {}grams".format(n))
        if n<2:
            return False
        if n==2:
            self.bigrams = pickle.load( open(pickle_file, 'rb') )
        if n==3:
            self.trigrams = pickle.load( open(pickle_file, 'rb') )
        print("loaded pickle...")

    # general ngrams saver to a pickle file
    def save_ngrams_pickle(self, pickle_file = "ngramdata/2grams.ng", n=2):
        print("saving into pickle...")
        if n<2:
            return False
        if n==2:
            pickle.dump(self.bigrams, open(pickle_file, "wb"))
        if n==3:
            pickle.dump(self.trigrams, open(pickle_file, "wb"))
        print("saved pickle...")

    """
    get integer count of the sequence of words
    seq : is a tuple of words
    returns count of occurences of such sequence
    """
    def get_count(self, seq):
        length = len(seq)
        if length>0 and length<=3:
            try:
                if length==2:
                    return self.bigrams.get(seq, 0)
                if length==3:
                    return self.trigrams.get(seq, 0)
            except KeyError:
                return 0
        else:
            return 0

    def get_probablity(self, seq):
        pass

def main():
    ngram = Ngram()
    start = time.time()

    """ load from text files -> very slow """
    #ngram.load_bigrams()
    #ngram.load_trigrams()
    #ngram.load_all()


    """ load from pickles -> very fast """
    ngram.load_ngrams_pickle(pickle_file="ngramdata/2grams.ng", n=2)
    ngram.load_ngrams_pickle(pickle_file="ngramdata/3grams.ng", n=3)

    """ save into pickle """
    #ngram.save_ngrams_pickle(pickle_file="ngramdata/3grams.ng",n=3)

    # print the time
    print(time.time() - start)

    # just a ngram tester
    while True:
        seq = str(input("enter sequence of words: "))
        if seq=="exit":
            break
        seq = seq.split()
        seq = tuple(seq)
        print("count for given seqence: {}".format(ngram.get_count(seq)) )


if __name__=="__main__":
    main()

