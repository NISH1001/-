<<<<<<< HEAD

from raw_translator.raw_translator import RawTranslator


translator = RawTranslator("data/dictionary.db")
print(translator.translate(input('nepali_text')))
=======
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
    #translator = RT.RawTranslator("dictionary/dictionary.db")

    while True:
        seq = input("enter sequences: ")
        seq = tuple(seq.split())
        sentence = ng.generate_sentence(seq)
        print(sentence)

    ng.close_ngramdb()

if __name__=="__main__":
    main()

>>>>>>> db07d334fb0ce5c4b8330161a087b83ee9500cc5
