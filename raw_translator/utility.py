import re
import json

class UtilityError(Exception):
    def __init__(self, args):
        self.args = args

    def Display(self):
        print("UtilityError: " + ''.join(self.args))


class Utility(object):
    def __init__(self):
        verbs = open("data/verb_tenses.json", 'r')
        verbs = verbs.read()
        self.verb_tenses = json.loads(verbs)

        nepeng = open("data/nepeng.json", "r")
        nepeng = nepeng.read()
        self.nep_eng = json.loads(nepeng)

    def is_nepali(text):
        #for now just check if eng chars are not present 
        for x in range(ord('a'), ord('z')+1):
            if chr(x) in text: return False
        for x in range(ord('A'), ord('Z')+1):
            if chr(x) in text: return False
        return True
 

    def get_tense(self, root_verb, simple_tense, non_simple_tense=None, singular=False, being_verb=False, negative=False):
        return_word = ""
        if being_verb:
            if(simple_tense=="past"):
                return_word = "was^^were^^had"
            elif (simple_tense=="present"):
                return_word= "am^^is^^are^^have^^has"
            else:
                return_word =  "will be"
        if non_simple_tense=='continuous':
            if simple_tense=='present':
                if singular: return_word= "is "+self.verb_tenses[root_verb]['continuous']
                else: return_word= "are^^am "+self.verb_tenses[root_verb]['continuous']
            if simple_tense=='past':
                if singular: return_word ="was "+self.verb_tenses[root_verb]['continuous']
                else: return_word= "were "+self.verb_tenses[root_verb]['continuous']
            if simple_tense=='future':
                return_word= "will be "+self.verb_tenses[root_verb]['continuous']

        elif non_simple_tense=='perfect':
            if simple_tense=='present':
                if singular: return_word= "has "+self.verb_tenses[root_verb]['perfect']
                else: return_word= "have "+self.verb_tenses[root_verb]['perfect']
            if simple_tense=='past':
                return_word= "had "+self.verb_tenses[root_verb]['perfect']
            if simple_tense=='future':
                return_word= "will have "+self.verb_tenses[root_verb]['perfect']

        elif non_simple_tense=='perfect continuous':
            if simple_tense=='present':
                if singular: return_word= "has been "+self.verb_tenses[root_verb]['continuous']
                else: return_word= "have been "+self.verb_tenses[root_verb]['continuous']
            if simple_tense=='past':
                return_word= "had been "+self.verb_tenses[root_verb]['continuous']
            if simple_tense=='future':
                return_word= "will have been "+self.verb_tenses[root_verb]['continuous']
        else:
            if simple_tense=="present":
                if singular: return_word= self.verb_tenses[root_verb]['singular']
                else: return_word= root_verb
            if simple_tense=='past':
                return_word= self.verb_tenses[root_verb]['past']
            if simple_tense=='future':
                return_word= "will " + root_verb

            if negative:
                return return_word + " not"


    def process_suffix(self, nepali_word):
        # first check for ले,बाट, tira, mathi, like naam 
        self.suffices = []
        for suffix in self.suffices:
            res = re.search('(\S+)'+suffix+'$', nepali_word)
            if res is not None:
                new_word = res.group(1)
                # check for 'हरु' in new_word
                res = re.search('(\S+)हरु$', new_word)
                if res is not None:
                    word = res.group(1)
                    return self.plural(self.dictionary_db_handler.get_english(word))
                return self.dictionary_db_handler.get_english(word)
        return []


    def plural(self, eng):
        return eng+'s'


    def get_eng_verb(self, nepali_root):
        possibles = []
        if re.search('(\S+)नु$', nepali_root):
            possibles = [nepali_root]
        elif re.search('(\S+)उ$', nepali_root):
            possibles = [nepali_root+'नु']
        elif re.search('(\S+)र्$', nepali_root):
            possibles = [nepali_root+'नु']
        elif re.search('(\S+)र$', nepali_root):
            possibles = [nepali_root+'्नु']
        else:
            possibles = [nepali_root+'नु', nepali_root+'उनु']
        return self.get_from_dict(possibles)
    
    def get_from_dict(self, possibles):
        for x in possibles:
            if self.nep_eng.get(x, '') != '':
                return self.nep_eng[x]
        return None
