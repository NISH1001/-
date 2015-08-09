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
        self.tense_structures = [] # initialize with the tenses
        self.simple_present = []
        self.simple_past = []
        self.simple_future = []
        self.simple_tenses = [self.simple_present, self.simple_past, self.simple_future]
        self.continuous = []
        self.perfect = []
        self.perfect_continuous = []
        self.non_simple_tenses = [self.continuous, self.perfect, self.perfect_continuous]
    
    def translate(self, nepali_text):
        try:
            # The whole portion of code below may be required to
            #   be modified later in other phases

            words = nepali_text.split()
            bigrams = [' '.join(words[x:x+2]) for x in range(len(words)-1)]

            # Check each ngram whether it is action or not 
            # In the first phase, we check for actions involving biphrases
            # After that, we check for single ones

            '''
            for i, item in enumerate(bigrams):
                eng_phrase = self.get_action(item) # checks bigram
                if eng_phrase is not None: # means phrase match found
                    re.sub(item, eng_phrase, nepali_text, 1)
            '''

            # now the biphrases are sustituted, we perform one by one translation of nepali words
            words = nepali_text.split()
            eng_words = []

            for x in words:
                if 1 or is_nepali(x): # **** 1 is just for debugging
                    eng_word = '^^'.join(list(
                            map(lambda x: x.lower(), self.dict_handler.get_english(x))
                            )
                        ) # CNF separated by ^^

                    if eng_word=='': # which is the case when no meaning found in dict
                        eng_word==get_action(x) # checks unigram

                    eng_words.append(eng_word)
                else:
                    eng_words.append(x.lower())

            return ' '.join(eng_words)

        except Exception:
            print('error occured')
            assert False

    def get_action(self, nepali_phrase): # nepali phrase is bigram/unigram for now
        # Check if the bigram matches any form in our tenses    
        for simple_tense in self.simple_tenses:
            for structure in simple_tense:

                # Check if the phrase's second part matches fully with the structure
                # If so it is not only simple, check first part too
                simple_result = re.search(' ('+structure+')', nepali_phrase)

                if simple_result is not None:
                    # Search for match in the first part of the phrase
                    first_part = nepali_phrase.split()[0]
                    # Now check in continuous, perfect and perfect continuous lists
                    for non_simple in self.non_simple_tenses:
                        # Here, full part won't match, so check partial
                        for each in non_simple:
                            non_simple_result = re.search('(\S)'+structure, first_part)
                            
                            if non_simple_result is None:
                                raise Exception('either phrase is wrong, or internal error while parsing :', nepali_phrase)

                            # Here, we have the verb root in non_simple_root, so extract verb
                            verb = extract_verb(non_simple_result.group(1))

                            return '' # here return the correct tense of the verb

                # Else if the simple_result returned none, which means, we check only the partial part
                else:
                    simple_result = re.search(' (\S)'+structure, nepali_phrase)
                    if simple_result is None:
                        return None # The phrase is not an action
                        raise Exception('either phrase is wrong, or internal error while parsing :', nepali_phrase)
                    verb = extract_verb(simple_result.group(1))
                    return '' # return the correct tense of the verb
                        

        pass
        


def main():
    translator = RawTranslator("dictionary/dictionary.db")
    print(translator.translate("खाना राम्रो"))


if __name__=='__main__':
    main()
