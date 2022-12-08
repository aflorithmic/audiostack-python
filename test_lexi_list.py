import audiostack
import os

audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]

dicts = audiostack.Speech.Diction.list()
for d in dicts:
    print(d.lang, d.content, d.words[0:10])


dicts = audiostack.Speech.Diction.Custom.list()
for d in dicts:
    print(d.lang, d.content, d.words[0:10])


create = audiostack.Speech.Diction.Custom.create_word("AFLR", "aflorithmic")
print(create)

word_sets = audiostack.Speech.Diction.Custom.list_words(lang="global")
for w in word_sets:
    print(w.inputs, w.replacements)
