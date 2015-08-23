import json
import re
from dictionary.DictionaryDBHandler import DictionaryDBHandler

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

def is_nepali(text):
    #for now just check if eng chars are not present 
    for x in range(ord('a'), ord('z')+1):
        if chr(x) in text: return False
    for x in range(ord('A'), ord('Z')+1):
        if chr(x) in text: return False
    return True
    

class RawTranslator(object):

    def __init__(self, db):
        self.dict_handler = DictionaryDBHandler(db)

        verbs = open("data/verb_tenses.json", 'r')
        verbs = verbs.read()
        self.verb_tenses = json.loads(verbs)

        rules = open("data/Rule.json", "r")
        rules = rules.read()
        self.tense_structures = json.loads(rules)

        nepeng = open("data/nepeng.json", "r")
        nepeng = nepeng.read()
        self.nep_eng = json.loads(nepeng)
    

    def translate(self, nepali_text):
        try:
            # The whole portion of code below may be required to
            #   be modified later in other phases

            words = nepali_text.split()
            bigrams = [' '.join(words[x:x+2]) for x in range(len(words)-1)]
            trigrams = [' '.join(words[x:x+3]) for x in range(len(words-2))] # not used now

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
                if is_nepali(x): # **** 1 is just for debugging
                    eng_word = '^^'.join(list(
                            map(lambda x: x.lower(), self.dict_handler.get_english(x))
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
            print(''.join(e.args))


    def get_action(self, nepali_phrase): # nepali phrase is bigram/unigram for now
        # Check if the bigram matches any form in our tenses    
        for simple_tense in self.tense_structures["Simple"]:
            for structure in self.tense_structures["Simple"][simple_tense]:

                # Check if the phrase's last part matches fully with the structure
                # If so it is not only simple, check remaining first part too
                simple_result = re.search(' ('+structure+')', nepali_phrase)

                if simple_result is not None:

                    #print("it is non simple tense...", simple_result.group(1))
                    #print(simple_tense, structure, simple_result.group(0))

                    # Search for match in the first part of the phrase
                    first_part = nepali_phrase.split()[0]
                    # Now check in continuous, perfect and perfect continuous lists
                    for non_simple_tense in self.tense_structures["NonSimple"]:
                        # Here, full part won't match, so check partial
                        for each in self.tense_structures["NonSimple"][non_simple_tense]:
                            non_simple_result = re.search('(\S+)'+each+'$', first_part)
                            if non_simple_result is not None: 

                                #print("bibek", non_simple_tense, each, non_simple_result.group(1))
                                # Here, we have the verb root in non_simple_root, so extract verb
                                root_verb = self.get_eng_verb(non_simple_result.group(1))

                                return self.get_tense(root_verb, simple_tense, non_simple_tense) # here return the correct tense of the verb

                    # it means no non-simple structure found like in म घर छु।
                    # return the first part and tense of second part e.g return 'घर am'
                    return first_part + self.get_tense(simple_result.group(1), simple_tense) 

        # Since non simple results not found, check simple only
        for simple_tense in self.tense_structures["Simple"]:
            for structure in self.tense_structures["Simple"][simple_tense]:
                simple_result = re.search('(\S+)'+structure+'$', nepali_phrase)
                if simple_result is not None:

                    #print(simple_tense, structure, simple_result.group(1))

                    # check for two possibilities: single word nep_verb
                    #                              double word nep_verb
                    root_verb = self.get_eng_verb(simple_result.group(1)) # double_word
                    if root_verb is not None:
                        return self.get_tense(root_verb, simple_tense) # return the correct tense of the verb
                    else:
                        root_verb = self.get_eng_verb(simple_result.group(1).split()[1]) # single word verb
                        if root_verb is not None:
                            return nepali_phrase.split()[0]+ ' '+self.get_tense(root_verb, simple_tense)
        return None

    def get_eng_verb(self, nepali_root):
        possibles = []
        if re.search('(\S+)नु$', nepali_root):
            possibles = [nepali_root]
        elif re.search('(\S+)उ$', nepali_root):
            possibles = [nepali_root+'नु']
        elif re.search('(\S+)र्$', nepali_root):
            possibles = [nepali_root+'नु']
        else:
            possibles = [nepali_root+'नु', nepali_root+'उनु']
        return self.get_from_dict(possibles)
    
    def get_from_dict(self, possibles):
        for x in possibles:
            if self.nep_eng.get(x, '') != '':
                return self.nep_eng[x]
        return None

    def get_tense(self, root_verb, simple_tense, non_simple_tense=None, singular=False):
        if non_simple_tense=='continuous':
            if simple_tense=='present':
                if singular: return "is "+self.verb_tenses[root_verb]['continuous']
                else: return "are "+self.verb_tenses[root_verb]['continuous']
            if simple_tense=='past':
                if singular: return "was "+self.verb_tenses[root_verb]['continuous']
                else: return "were "+self.verb_tenses[root_verb]['continuous']
            if simple_tense=='future':
                return "will be "+self.verb_tenses[root_verb]['continuous']

        elif non_simple_tense=='perfect':
            if simple_tense=='present':
                if singular: return "has "+self.verb_tenses[root_verb]['perfect']
                else: return "have "+self.verb_tenses[root_verb]['perfect']
            if simple_tense=='past':
                return "had "+self.verb_tenses[root_verb]['perfect']
            if simple_tense=='future':
                return "will have "+self.verb_tenses[root_verb]['perfect']

        elif non_simple_tense=='perfect continuous':
            if simple_tense=='present':
                if singular: return "has been "+self.verb_tenses[root_verb]['continuous']
                else: return "have been "+self.verb_tenses[root_verb]['continuous']
            if simple_tense=='past':
                return "had been "+self.verb_tenses[root_verb]['continuous']
            if simple_tense=='future':
                return "will have been "+self.verb_tenses[root_verb]['continuous']
        else:
            if simple_tense=="present":
                if singular: return self.verb_tenses[root_verb]['singular']
                else: return root_verb
            if simple_tense=='past':
                return self.verb_tenses[root_verb]['past']
            if simple_tense=='future':
                return "will " + root_verb


def main():
    translator = RawTranslator("dictionary/dictionary.db")
    n = input('enter nepali sentence ')
    while(n!='==='):
        print(translator.translate(n))
        n = input('enter nepali sentence ')
    print("end")


if __name__=='__main__':
    main()
