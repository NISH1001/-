import json
import re
from dictionary.dictionary_db_handler import DictionaryDBHandler
from raw_translator.utility import *

class RawTranslatorError(Exception):
    def __init__(self, args):
        self.args = args

    def Display(self):
        print("RawTranslatorError: " + ''.join(self.args))

'''
what remain:
-singular/plural
-imperative forms
'''

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

        rules = open("data/Rule.json", "r")
        rules = rules.read()
        self.tense_structures = json.loads(rules)

        self.utility = Utility()
            
    
    def translate(self, nepali_text):
        try:
            # The whole portion of code below may be required to
            #   be modified later in other phases

            words = nepali_text.split()
            bigrams = [' '.join(words[x:x+2]) for x in range(len(words)-1)]

            # Check each ngram whether it is action or not 
            # In the first phase, we check for actions involving biphrases

            for i, item in enumerate(bigrams):
                eng_phrase = self.get_action(item) # checks bigram if it is action
                print('nepali:',item, eng_phrase)

                if eng_phrase is not None: # means phrase match found
                    # replace the phrase with english equivalent
                    nepali_text = re.sub(item, eng_phrase, nepali_text, 1)

            # now the biphrases are sustituted, we perform one by one translation of nepali words
            words = nepali_text.split()
            eng_words = []

            for x in words:
                if Utility.is_nepali(x): 
                    eng_meanings = self.dict_handler.get_english(x)

                    if len(eng_meanings) == 0:
                        # process for हरु, मा, बाट, ले, and so on
                        eng_meanings = self.utility.process_suffix(x)
                        pass

                    eng_word = '^^'.join(list(
                            map(lambda a: a.lower(), eng_meanings)
                            )
                        ) # CNF separated by ^^

                    '''
                    if eng_word=='': # which is the case when no meaning found in dict
                        eng_word==get_action(x) # checks unigram
                    '''

                    eng_words.append(eng_word)
                else:
                    eng_words.append(x.lower())

            return ' '.join(eng_words)

        except Exception as e:
            print('Error in raw_translator: '+''.join(e.args))


    def get_action(self, nepali_phrase): # nepali phrase is bigram/unigram for now
        # Check if the bigram matches any form in our tenses    
        for simple_tense in self.tense_structures["Simple"]:
            for structure in self.tense_structures["Simple"][simple_tense]:
                
                struc_process = re.match('([^a-z]+)([a-z]*)', structure)
                structure_tags = struc_process.group(2)
                actual_str = struc_process.group(1)
                #actual_str = structure

                # Check if the phrase's last part matches fully with the structure
                # If so it is not only simple, check remaining first part too
                simple_result = re.search(' ('+actual_str+')$', nepali_phrase)

                if simple_result is not None:

                    #print("it is non simple tense...", simple_result.group(1))
                    #print(simple_tense, structure, simple_result.group(0))

                    # Search for match in the first part of the phrase
                    #first_part = nepali_phrase.split()[0]
                    remaining_part = re.sub(' ' +structure+'$', '', nepali_phrase)
                    # Now check in continuous, perfect and perfect continuous lists
                    for non_simple_tense in self.tense_structures["NonSimple"]:
                        # Here, full part won't match, so check partial
                        for each in self.tense_structures["NonSimple"][non_simple_tense]:
                            non_simple_result = re.search('(\S+)'+each+'$', remaining_part)
                            if non_simple_result is not None: 

                                #print("bibek", non_simple_tense, each, non_simple_result.group(1))
                                # Here, we have the verb root in non_simple_root, so extract verb
                                root_verb = self.utility.get_eng_verb(non_simple_result.group(1))

                                return self.utility.get_tense(root_verb, simple_tense, non_simple_tense) # here return the correct tense of the verb

                    # it means no non-simple structure found like in म खतरा  छु।
                    # return the first part and tense of second part e.g return 'खतरा  am'
                    return first_part +' '+ self.utility.get_tense(simple_result.group(1), simple_tense, being_verb=True) 

        # Since non simple results not found, check simple only
        for simple_tense in self.tense_structures["Simple"]:
            for structure in self.tense_structures["Simple"][simple_tense]:
                
                neg = False

                struc_process = re.match('([^a-z]+)([a-z]*)', structure)
                structure_tags = struc_process.group(2)
                actual_str = struc_process.group(1)

                simple_result = re.search('(.+)'+actual_str+'$', nepali_phrase)
                #print(nepali_phrase, structure, structure in nepali_phrase)
                if simple_result is not None:

                    if 'n' in structure_tags:
                        neg=True

                    # check for two possibilities: single word nep_verb
                    #                              double word nep_verb
                    root_verb = self.utility.get_eng_verb(simple_result.group(1)) # double_word
                    if root_verb is not None:
                        return self.utility.get_tense(root_verb, simple_tense, negative=neg) # return the correct tense of the verb
                    else:
                        root_verb = self.utility.get_eng_verb(simple_result.group(1).split()[-1] ) # single word verb
                        if root_verb is not None:
                            return nepali_phrase.split()[0]+ ' '+self.utility.get_tense(root_verb, simple_tense, negative=neg)
        return None


    
def main():
    translator = RawTranslator("data/dictionary.db")
    n = input('enter nepali sentence ')
    while(n!='==='):
        print(translator.translate(n))
        n = input('enter nepali sentence ')
    print("end")


if __name__=='__main__':
    main()
