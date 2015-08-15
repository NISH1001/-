import re
from dictionary.DictionaryDBHandler import DictionaryDBHandler

class RawTranslatorError(Exception):
    def __init__(self, args):
        self.args = args

    def Display(self):
        print("RawTranslatorError: " + ''.join(self.args))


"""
RawTranslator class:
--  Performs word-to-word or phrase-to-phrase translation
    for performing further probabilistic processing
--  Requires access to the bilingual dictionary and, phrases and 
    idioms translation database
--  Needs to access the list of all the verb forms in nepali languages
    and 'nipaats' and some other parts of nepali sentences

attributes:
    ...

methods:
    ...
"""

class RawTranslator(object):

    def __init__(self, db):
        self.dict_handler = DictionaryDBHandler(db)
    
    def translate(self, nepali_text):
        try:
            #   be modified later in other phases

            # The whole portion of code below may be required to
            words = nepali_text.split()
            bigrams = [' '.join(words[x:x+2]) for x in range(len(words)-1)]

            # Check each ngram whether it is action or not 

            '''
            for i, item in enumerate(bigrams):
                eng_phrase = get_english_eqv(item)
                if eng_phrase is not None: # means phrase match found
                    re.sub(item, eng_phrase, nepali_text, 1)
            '''

            # now the biphrases are sustituted, we perform one by one translation of nepali words
            words = nepali_text.split()
            eng_words = []

            for x in words:
                if 1 or is_nepali(x): # **** 1 is just for debugging
                    eng_words.append('^^'.join(list(
                            map(lambda x: x.lower(), self.dict_handler.get_english(x))
                            )
                        )
                    ) # CNF separated by ^^
                else:
                    eng_words.append(x.lower())

            return ' '.join(eng_words)

        except Exception:
            print('error occured')
            assert False

    def get_eng_eqv(self, nepali_phrase):
        pass


def main():
    translator = RawTranslator("dictionary/dictionary.db")
    print(translator.translate("घर जाउ"))


if __name__=='__main__':
    main()
