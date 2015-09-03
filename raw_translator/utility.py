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

        neg = pres_neg= past_neg= ""
        if negative: 
            neg="not"
            pres_neg='do not'
            past_neg='did not'


        if being_verb:
            if(simple_tense=="past"):
                return  "was^^were^^had "+ neg
            elif (simple_tense=="present"):
                return  "am^^is^^are^^have^^has " + neg
            else:
                return "will "+neg+" be"

        if non_simple_tense=='continuous':
            if simple_tense=='present':
                if singular: return "is "+neg+' '+self.verb_tenses[root_verb]['continuous']
                else: return "are^^am "+neg+' '+self.verb_tenses[root_verb]['continuous']
            if simple_tense=='past':
                if singular: return "was "+neg+' '+self.verb_tenses[root_verb]['continuous']
                else: return "were "+neg+' '+self.verb_tenses[root_verb]['continuous']
            if simple_tense=='future':
                return "will "+neg+" "+"be "+self.verb_tenses[root_verb]['continuous']

        elif non_simple_tense=='perfect':
            if simple_tense=='present':
                if singular: return "has "+neg+' '+self.verb_tenses[root_verb]['perfect']
                else: return "have "+neg+' '+self.verb_tenses[root_verb]['perfect']
            if simple_tense=='past':
                return "had "+neg+' '+self.verb_tenses[root_verb]['perfect']
            if simple_tense=='future':
                return "will "+neg+' '+"have "+self.verb_tenses[root_verb]['perfect']

        elif non_simple_tense=='perfect continuous':
            if simple_tense=='present':
                if singular: return "has "+neg+" been "+self.verb_tenses[root_verb]['continuous']
                else: return "have "+neg+" been "+self.verb_tenses[root_verb]['continuous']
            if simple_tense=='past':
                return "had "+neg+" been "+self.verb_tenses[root_verb]['continuous']
            if simple_tense=='future':
                return "will "+neg+" have been "+self.verb_tenses[root_verb]['continuous']
        else:
            if simple_tense=="present":
                if singular: return pres_neg+' '+self.verb_tenses[root_verb]['singular']
                else: return pres_neg+' '+root_verb
            if simple_tense=='past':
                if negative: return past_neg+' '+root_verb
                else: return self.verb_tenses[root_verb]['past']
            if simple_tense=='future':
                return "will "+neg+' ' + root_verb


    
    def check_plural(self, nepali_word):
        res = re.search('(\S+)हरु$', nepali_word)
        if res is not None:
            return (True, res.group(1))
        return(False, nepali_word)

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
