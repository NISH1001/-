import json
import re
from dictionary.dictionary_db_handler import DictionaryDBHandler
from raw_translator.utility import *

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
"""
   

class RawTranslator(object):

    def __init__(self, db):
        self.dict_handler = DictionaryDBHandler(db)

        rules = open("data/Rule.json", "r")
        rules = rules.read()
        self.tense_structures = json.loads(rules)

        suffices = open("data/suffices.json","r")
        self.suffices = json.loads(suffices.read())

        self.utility = Utility()

    
    def translate(self, nepali_text):
        #try:
            # The whole portion of code below may be required to
            #   be modified later in other phases

            words = nepali_text.split()
            bigrams = [' '.join(words[x:x+2]) for x in range(len(words)-1)]

            # Check each ngram whether it is action or not 
            # In the first phase, we check for actions involving biphrases

            for i, item in enumerate(bigrams):
                eng_phrase = self.get_action(item) # checks bigram if it is action

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
                        #print('in process suffix:')
                        temp = self.process_suffix(x)
                        if temp.strip()=='':
                            temp = self.further_process(x)
                        #print('processed :', type(temp), temp)
                        eng_words.append(temp)

                    else:
                        eng_word = '^^'.join(list(
                                map(lambda a: a.lower(), eng_meanings)
                                )
                            ) # CNF separated by ^^

                        eng_words.append(eng_word)
                else:
                    eng_words.append(x.lower())

            return ' '.join(eng_words)

        #except Exception as e:
            #print('Error in raw_translator: '+''.join(e.args))


    def get_action(self, nepali_phrase): # nepali phrase is bigram/unigram for now
        # Check if the bigram matches any form in our tenses    
        for simple_tense in self.tense_structures["Simple"]:
            for structure in self.tense_structures["Simple"][simple_tense]:
                
                struc_process = re.match('([^a-z]+)([a-z]*)', structure)
                structure_tags = struc_process.group(2)
                actual_str = struc_process.group(1)

                # Check if the phrase's last part matches fully with the structure
                # If so it is not only simple, check remaining first part too
                simple_result = re.search('[ ]+('+actual_str+')$', nepali_phrase)
                #print('checking: ', nepali_phrase, structure)
                neg = False
                if simple_result is not None:
                    #print('structure tags:', structure_tags)
                    if 'n' in structure_tags:
                        neg = True

                    # Search for match in the first part of the phrase
                    #first_part = nepali_phrase.split()[0]
                    remaining_part = re.sub(' ' +actual_str+'$', '', nepali_phrase)
                    # Now check in continuous, perfect and perfect continuous lists
                    for non_simple_tense in self.tense_structures["NonSimple"]:
                        # Here, full part won't match, so check partial
                        for each in self.tense_structures["NonSimple"][non_simple_tense]:
                            non_simple_result = re.search('(\S+)'+each+'$', remaining_part)
                            if non_simple_result is not None: 

                                #print("bibek", non_simple_tense, each, non_simple_result.group(1))
                                # Here, we have the verb root in non_simple_root, so extract verb
                                root_verb = self.utility.get_eng_verb(non_simple_result.group(1))
                                if not root_verb is None:

                                    return self.utility.get_tense(root_verb, simple_tense, non_simple_tense, negative=neg, singular='s' in structure_tags) 
                                # here return the correct tense of the verb

                    # it means no non-simple structure found like in म खतरा  छु।
                    # return the first part and tense of second part e.g return 'खतरा  am'
                    verb = self.utility.get_tense(simple_result.group(1), simple_tense, being_verb='b' in structure_tags) 
                    if verb is not None:
                        return remaining_part+' '+ verb
                    else: return None

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
                    #print('match_simple')

                    if 'n' in structure_tags:
                        neg=True

                    # check for two possibilities: single word nep_verb
                    #                              double word nep_verb
                    nep_verb_part = simple_result.group(1)
                    if nep_verb_part=='':continue
                    root_verb = self.utility.get_eng_verb(simple_result.group(1)) # double_word
                    #print('root_verb: ', root_verb)
                    if root_verb is not None:
                        return self.utility.get_tense(root_verb, simple_tense, negative=neg, singular='s' in structure_tags) 
                        # return the correct tense of the verb
                    else:
                        root_verb = self.utility.get_eng_verb(simple_result.group(1).split()[-1] ) # single word verb
                        if root_verb is not None:
                            return nepali_phrase.split()[0]+ ' '+self.utility.get_tense(root_verb, simple_tense, negative=neg, singular='s' in structure_tags)
                        else:
                            return nepali_phrase#since no verb found, return as it is for other words may match it
                            raise RawTranslatorError('No verb found for  '+ nepali_phrase)
        return None


    def process_suffix(self, nepali_word):
        words = None
        suffx_meanings = None

        # check 'ko' at the end
        res = re.search('(\S+)को$', nepali_word)
        if res is not None:
            new_word = res.group(1)
            plural_result = self.utility.check_plural(new_word)
            if plural_result[0]:
                words = list(map(self.utility.plural, self.dict_handler.get_english(plural_result[1])))
                words = [x+"'" for x in words]
                return '^^'.join(words)
            else:
                return '^^'.join([x+"'s" for x in self.dict_handler.get_english(new_word)])

        # first check if हरु exist or not
        plural_result = self.utility.check_plural(nepali_word)
        if plural_result[0]:
            words = list(map(self.utility.plural, self.dict_handler.get_english(plural_result[1])))
            # if haru exist at last, return plural
            return '^^'.join(words)

        
        # if not then check for ले,बाट, tira, mathi, like naam 
        for suffix in self.suffices:
            res = re.search('(\S+)'+suffix.strip()+'$', nepali_word)
            if res is not None:
                new_word = res.group(1)
                suffx_meanings = self.suffices.get(suffix, '') # meanings of ले, तर्फ, etc
                # check for 'हरु' in new_word, which might still be present like in घरहरुले
                plural_result = self.utility.check_plural(new_word) 
                if plural_result[0]:
                    words = list(map(self.utility.plural, self.dict_handler.get_english(plural_result[1]))) 
                else:
                    words = self.dict_handler.get_english(new_word)

        if suffx_meanings is not None and words is not None:
            return '^^'.join(suffx_meanings) + ' ' + '^^'.join(words)
        elif words is not None:
            return '^^'.join(words)
        else: return ''

    def further_process(self, nepali_string):
        #print('in further process')
        # here, check for various possible structures of words 
        neg = ''

        # first check for imperative ones
        new = nepali_string

        new = re.sub('(होस्)$','',nepali_string)
        new = re.sub('(स्)$','', new)
        new = re.sub('(ऊ)$', 'उ', new) # like khau, jau, which have dirgha wookar
        if re.match('^न', new):
            neg = 'do not'
            new = re.sub('^न', '', new)
        #new = re.sub('(ू)$', 'ु', new) # like khau, jau, which have dirgha wookar

        r = self.utility.get_eng_verb(new)
        if r is not None and r is not '':
            return neg+' '+r

        # do search in non simple tenses
        for non_simple_tense in self.tense_structures["NonSimple"]:
            # Here, full part won't match, so check partial
            for each in self.tense_structures["NonSimple"][non_simple_tense]:
                non_simple_result = re.search('(\S+)'+each+'$', nepali_string)

                if non_simple_result is not None: 
                        # Here, we have the verb root in non_simple_root, so extract verb
                            root_verb = self.utility.get_eng_verb(non_simple_result.group(1))
                            if root_verb is not None:
                                return Utility.verb_tenses[root_verb][non_simple_tense]
                                #return self.utility.get_tense(root_verb, simple_tense, non_simple_tense, negative=neg, singular='s' in structure_tags) 


    
def main():
    translator = RawTranslator("data/dictionary.db")
    n = input('enter nepali sentence ')
    while(n!='==='):
        print(translator.translate(n))
        n = input('enter nepali sentence ')
    print("bye bye")


if __name__=='__main__':
    main()
