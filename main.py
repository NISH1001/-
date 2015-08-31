import sqlite3
from raw_translator.raw_translator import RawTranslator
from dictionary.dictionary_db_handler import DictionaryDBHandler


#!/usr/bin/env python3

# load our packages
from ngram import ngram
from raw_translator import raw_translator as RT
import time

def main():
    start = time.time()

    ''' ngram object : loadtype=memory '''
    ng = ngram.Ngram(data_path="data/ngrams/", load_type="memory")

    print(time.time() - start)

    ''' translator object : i dont have verbs_tense.json '''
    translator = RawTranslator("data/dictionary.db")

    while True:
        nepali = input("nepali: ")
        if nepali=="===":
            break
        cnf = translator.translate(nepali)
        print("original cnf : {}".format(cnf))

        sentences = ng.cnf_separator(cnf)
        for sentence in sentences:
            print(sentence)

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

        print(dicthandler.get_english1('राम्रो'))
    except Exception as e:
        print(e)

if __name__=="__main__":
    main()
    #test_dict()
