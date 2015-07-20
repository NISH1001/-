import goslate
import json

# We have nepali uincode words here
nepali_words = []

# Dictionary to hold words and meanings
nepali_english = {}

# Goslate object to translate
go = goslate.Goslate()

for word in nepali_words:
    nepali_english[word] = go.translate(word, 'ne')

# We now have the required dictionary in nepali_english
