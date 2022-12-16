import audiostack
import os

audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]

# res = audiostack.Content.Media.create(filePath="Timo.mp3")
# print(res.response)

scriptTxt = """
<<soundSegment::intro>><<sectionName::intro>> Hello Sam how are you? 
<<soundSegment::main>> <<sectionName::main>> This is main <<media::media1>>
<<soundSegment::outro>><<sectionName::outro>> goodbye
"""

scriptItem = audiostack.Content.Script.create(scriptText=scriptTxt)
print(scriptItem.response)
speechItem = audiostack.Speech.TTS.create(scriptItem=scriptItem, voice="Sara")
print(speechItem)
mixItem = audiostack.Production.Mix.create(speechItem=speechItem, soundTemplate="vinylhits", mediaFiles={"media1" : "27cae14a"})
print(mixItem)
mixItem.download()


#27cae14a


# mediaFiles = audiostack.Content.Media.list()
# for m in mediaFiles:
#     r = m.delete()
#     print(r.message)

# dicts = audiostack.Speech.Diction.list()
# for d in dicts:
#     print(d.lang, d.content, d.words[0:10])


# dicts = audiostack.Speech.Diction.Custom.list()
# for d in dicts:
#     print(d.lang, d.content, d.words[0:10])


# create = audiostack.Speech.Diction.Custom.create_word("AFLR", "aflorithmic")
# print(create)

# word_sets = audiostack.Speech.Diction.Custom.list_words(lang="global")
# for w in word_sets:
#     print(w.inputs, w.replacements)
