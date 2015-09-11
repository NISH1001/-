#!/usr/bin/env python3

# inbuilt packages/moduels
import sqlite3
import sys
from raw_translator.raw_translator import RawTranslator
from dictionary.dictionary_db_handler import DictionaryDBHandler
import time

# load our packages
from raw_translator.raw_translator import RawTranslator
from dictionary.dictionary_db_handler import DictionaryDBHandler
from ngram import ngram
from raw_translator import raw_translator as RT
from utilities import cnf_separator

def get_input():
    # main loop
    while True:
        print("-"*80)
        nepali = input("nepali: ")
        if nepali=="===":
            break
        cnf = translator.translate(nepali)
        #print("original cnf : {}".format(cnf))

        # get separated sentence list using the cnf forms
        separated = cnf_separator(cnf)

        sentences = ng.generate_sentences_from_list(separated)
        #print("possible synonym sentences : ")
        #for sentence in sentences:
        #    print(sentence)
        best = ng.generate_sentence_best(sentences)
        print("Translated : ", ' '.join(best))

    print("exiting...")


def main():
    start = time.time()

    ''' ngram object : loadtype=memory '''
    ng = ngram.Ngram(data_path="data/ngrams/", load_type="memory")

    print(time.time() - start)

    ''' translator object : i dont have verbs_tense.json '''
    translator = RawTranslator("data/dictionary.db")

    while True:
        print("-"*80)
        nepali = input("nepali: ")
        if nepali=="===":
            break
        try:
            cnf = translator.translate(nepali)
            #print("original cnf : {}".format(cnf))

            # get separated sentence list using the cnf forms
            separated = cnf_separator(cnf)

            sentences = ng.generate_sentences_from_list(separated)
            #print("possible synonym sentences : ")
            #for sentence in sentences:
            #    print(sentence)
            best = ng.generate_sentence_best(sentences)
            print("Translated : ", ' '.join(best))
        except Exception as e:
            print(repr(e))
            continue

    print("exiting...")

    ng.close_ngramdb()

def test_dict():
    try:
        dicthandler = DictionaryDBHandler("data/dictionary.db")
        print("enter == to exit.. ")
        i = input("enter nepali unigram and meaning separated by comma: ")
        while i != '==':
            splitted = i.split(',')
            dicthandler.insert_unigram(splitted[0], tuple(splitted[1:len(splitted)]))
            i = input("enter nepali unigram and meaning separated by spaces: ")

        #print(dicthandler.get_english1('राम्रो'))
    except Exception as e:
        print(e)

if __name__=="__main__":
    args = sys.argv[1]
    if args=="train":
        test_dict()
    elif args=="translate":
        main()
    else:
        print("Usage: suported arguments are 'train' and 'translate'")
