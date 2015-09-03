#!/usr/bin/env python3

import re
import codecs
import time
from collections import defaultdict, OrderedDict
import pickle
import operator

"""
    A class for operating all the ngram things in memory (not database)

functions:
    count()     : it is our main function that returns the count 
"""
class NgramMem(object):

    def __init__(self, data_path="../data/ngrams/"):
        self.unigrams = OrderedDict()
        self.bigrams  = OrderedDict()
        self.trigrams = OrderedDict()
        self.quadgrams = OrderedDict()
        self.data_path = data_path
        self.aggregate_sum = [0, 286758206,128125547, 46030908]

    # load all the ngrams dict from text files
    def load_all(self, pickle=True):
        if not pickle:
            self.load_bigrams(file_ngrams=self.data_path+"2grams.txt")
            self.load_trigrams(file_ngrams=self.data_path+"3grams.txt")
            #self.load_quadgrams(file_ngrams=self.data_path+"4grams.txt")
        else:
            self.load_ngrams_pickle(pickle_file=self.data_path+"2grams.ng", n=2)
            self.load_ngrams_pickle(pickle_file=self.data_path+"3grams.ng", n=3)
            #self.load_ngrams_pickle(pickle_file=self.data_path+"4grams.ng", n=4)

    # load the bigrams from the desired file
    def load_bigrams(self, file_ngrams = "../data/ngrams/2grams.txt"):
        # codecs is used to remove conflicts with encoding schemes
        with codecs.open(file_ngrams, 'rb', encoding='utf-8', errors='ignore' ) as f:
            print("loading bigrams... from {}".format(file_ngrams))
            for line in f:
                splitted = line.split()
                self.bigrams[ (splitted[1], splitted[2]) ] = splitted[0]
        print("bigrams loaded successfully... :P")

    # load the trigrams
    def load_trigrams(self, file_ngrams = "../data/ngrams/3grams.txt"):
        # codecs is used to remove conflicts with encoding schemes
        with codecs.open(file_ngrams, 'rb', encoding='utf-8', errors='ignore' ) as f:
            print("loading trigrams... from {}".format(file_ngrams))
            for line in f:
                splitted = line.split()
                self.trigrams[ (splitted[1], splitted[2], splitted[3]) ] = splitted[0]
        print("trigrams loaded successfully... :P")

    # load the quadgrams
    def load_quadgrams(self, file_ngrams = "../data/ngrams/4grams.txt"):
        # codecs is used to remove conflicts with encoding schemes
        with codecs.open(file_ngrams, 'rb', encoding='utf-8', errors='ignore' ) as f:
            print("loading quadgrams... from {}".format(file_ngrams))
            for line in f:
                splitted = line.split()
                self.quadgrams[ (splitted[1], splitted[2], splitted[3], splitted[4]) ] = splitted[0]
        print("quadgrams loaded successfully... :P")

    def insert_into_db(self):
        """
        print("\ninserting into bigrams...")
        bg = []
        for key in self.bigrams:
            seq = list(key)
            seq.append(self.bigrams[key])
            seq = tuple(seq)
            bg.append(seq)
        self.ngramdb.insert_many(bg, n=2)
        """

        """
        print("\ninserting into trigrams table...")
        tg = []
        for key in self.trigrams:
            seq = list(key)
            seq.append(self.trigrams[key])
            seq = tuple(seq)
            tg.append(seq)
        self.ngramdb.insert_many(tg, n=3)
        """

        """
        print("\ninserting into quadgrams table...")
        qg = []
        for key in self.quadgrams:
            seq = list(key)
            seq.append(self.quadgrams[key])
            seq = tuple(seq)
            qg.append(seq)
        self.ngramdb.insert_many(qg, n=4)
        """
    # general ngrams loader from pickle file
    def load_ngrams_pickle(self, pickle_file = "../data/ngrams/2grams.ng", n=2):
        print("loading pickle... {}grams".format(n))
        if n<2:
            return False
        elif n==2:
            self.bigrams = pickle.load( open(pickle_file, 'rb') )
        elif n==3:
            self.trigrams = pickle.load( open(pickle_file, 'rb') )
        else:
            self.quadgrams = pickle.load( open(pickle_file, 'rb') )
        print("loaded pickle...")

    # general ngrams saver to a pickle file
    def save_ngrams_pickle(self, pickle_file = "../data/ngrams/2grams.ng", n=2):
        print("saving into pickle...")
        if n<2:
            return False
        elif n==2:
            pickle.dump(self.bigrams, open(pickle_file, "wb"))
        elif n==3:
            pickle.dump(self.trigrams, open(pickle_file, "wb"))
        else:
            pickle.dump(self.quadgrams, open(pickle_file, "wb"))
        print("saved pickle...")

    def count(self, seq, total=False):
        n = len(seq)
        ret = None
        if total:
            ret = self.aggregate_sum[n-1]
        else:
            try:
                if n==2:
                    ret = self.bigrams[seq]
                elif n==3:
                    ret = self.trigrams[seq]
                elif n==4:
                    ret = self.quadgrams[seq]
                else:
                    ret = 0
            except KeyError:
                ret = 0
        return int(ret)

    def count_vocab(self, n=2):
        if n==2:
            return len(self.bigrams)
        elif n==3:
            return len(self.trigrams)
        elif n==4:
            return len(self.quadgrams)
        else:
            return 0

def main():
    ngrammem = NgramMem()
    start = time.time()
    ngrammem.load_all(pickle=True)
    print(time.time()-start)

    # just a ngram tester
    while True:
        seq = str(input("enter sequence of words: "))
        if not seq:
            continue
        if seq=="exit":
            break
        seq = seq.split()
        seq = tuple(seq)
        print(ngrammem.probability(seq))


if __name__=="__main__":
    main()

