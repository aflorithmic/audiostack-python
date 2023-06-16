import audiostack
import os

audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]

# list words in default public dicts
dicts = audiostack.Speech.Diction.list()
for d in dicts:
    print(d.lang, d.content, d.words[0:10])

# list words in custom dicts
dicts = audiostack.Speech.Diction.Custom.list()
for d in dicts:
    print(d.lang, d.content, d.words[0:10])

# add word
create = audiostack.Speech.Diction.Custom.create_word(word="AFLR", replacement="aflorithmic", lang="global")
print(create)

# delete word
response = audiostack.Speech.Diction.Custom.delete_word(word="AFLR", lang="global")
print(response)

# list words and replacements in a custom dict
word_sets = audiostack.Speech.Diction.Custom.list_words(lang="global")
for w in word_sets:
    print(w.inputs, w.replacements)
