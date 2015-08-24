
from raw_translator.raw_translator import RawTranslator


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

if __name__=="__main__":
    main()
