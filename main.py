
from raw_translator.raw_translator import RawTranslator


translator = RawTranslator("data/dictionary.db")
print(translator.translate(input('nepali_text')))
