#!/usr/bin/env python3

import re
import codecs
import time
from collections import defaultdict, OrderedDict
import pickle
from ngramdb import NgramDB

"""
Ngram class: 
-- For now we we upto quadgrams

attributes:
    bigrams,trigrams,quadgrams are all dictionary with key as tuple of words
    eg: bigrams[('happy', 'man)] = somecount
"""
class Ngram(object):

    def __init__(self):
        self.unigrams = OrderedDict()
        self.bigrams  = OrderedDict()
        self.trigrams = OrderedDict()
        self.quadgrams = OrderedDict()

        # this is ngrams database handler
        self.ngramdb = NgramDB()
        #self.ngramdb.create_table_all()

    # load all the ngrams dict from text files
    def load_all(self, pickle=True):
        if not pickle:
            self.load_bigrams(file_ngrams="../data/ngrams/2grams.txt")
            self.load_trigrams(file_ngrams="../data/ngrams/3grams.txt")
            self.load_quadgrams(file_ngrams="../data/ngrams/4grams.txt")
        else:
            self.load_ngrams_pickle(pickle_file="../data/ngrams/2grams.ng", n=2)
            self.load_ngrams_pickle(pickle_file="../data/ngrams/3grams.ng", n=3)
            self.load_ngrams_pickle(pickle_file="../data/ngrams/4grams.ng", n=4)

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

    def close_ngramdb(self):
        self.ngramdb.close()

    """
    get integer count of the sequence of words
    seq : is a tuple of words
    returns count of occurences of such sequence
    """
    def count(self, seq):
        """
        length = len(seq)
        if length>0 and length<=4:
            try:
                if length==2:
                    return self.bigrams.get(seq, 0)
                elif length==3:
                    return self.trigrams.get(seq, 0)
                else:
                    return self.quadgrams.get(seq, 0)
            except KeyError:
                return 0
        else:
            return 0
        """

        length = len(seq)
        if length>1 and length<=4:
            # get count object ie sqlite cursor object
            # an iterator is actually returned
            count_obj = self.ngramdb.count(seq)
            # create list of tuples; here only one tuple for the count
            res = [ row for row in count_obj ] 
            if not res:
                return 0

            counter = res[0]
            return int(counter[0])

    def get_probablity(self, seq):
        pass

def main():
    ngram = Ngram()
    start = time.time()

    """ load ngrams : now not needed because of sqlite db """
    # load ngram from text/pickle files
    # ngram.load_all(pickle=True)

    """ save into pickle """
    #ngram.save_ngrams_pickle(pickle_file="../data/ngrams/2grams.ng",n=2)
    #ngram.save_ngrams_pickle(pickle_file="../data/ngrams/3grams.ng",n=3)
    #ngram.save_ngrams_pickle(pickle_file="../data/ngrams/4grams.ng",n=4)

    # print the time
    print("time : ",time.time() - start)

    # just a ngram tester
    while True:
        seq = str(input("enter sequence of words: "))
        if not seq:
            continue
        if seq=="exit":
            break
        seq = seq.split()
        seq = tuple(seq)
        print("count for the seqence: {}".format(ngram.count(seq)) )
        #print(ngram.count(seq))

    #ngram.insert_into_db()

    ngram.close_ngramdb()

if __name__=="__main__":
    main()

