import re

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
    def __init__(self, args):
        pass
    
    # at this phase no CNF, no synonyms, no idioms.
    def translate(self, nepali_text):
        try:
            # The whole portion of code below may be required to
            #   be modified later in other phases

            words = nepali_text.split()
            bigrams = [' '.join(words[x:x+2]) for x in range(len(words)-1)]

            # Check each ngram whether it is action or not 
            # if yes, convert it and remove the previous one from list

            for enumerate(item, i) in bigrams:
                eng_phrase = get_phrase(item)
                if eng_phrase is not None: # means phrase match found
                    re.sub(item, eng_phrase, nepali_text, 1)

            # now the biphrases are sustituted, we perform one by one translation of nepali words
            words = nepali_text.split()
            eng_words = []
            for x in words:
                if is_nepali(x):
                    eng_words.append(english_equivalent(x))
                else:
                    eng_words.append(x)

            return ' '.join(eng_words)
