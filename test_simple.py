import audiostack
import os

audiostack.api_base = "https://staging-v2.api.audio"
audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]

scriptText = """
<as:section name="intro" soundsegment="intro"> 
    hello this is the new script syntax 
</as:section>
<as:section name="main" soundsegment="main"> 
    This uses regular H T M L syntax and replaces our old script formatting 
</as:section>
<as:section name="outro" soundsegment="outro"> 
    This massively improves usability, aids with learnability and should improve adoption 
</as:section>"""

# scriptText = """

# <as:section name="main" soundsegment="main"> 
#     We now have a new feature in our mastering engine. As well as getting back a high quality, ready mixed audio asset, you can also request the isolated voice track. This is perfect for applications including chat bots.
# </as:section>
# """

# scriptText = """
# <as:section name="main" soundSegment="main">
#     This is the new awesome script section
#     <as:fx name="riser1"/>
#     this content is part of section main also
# </as:section>


# <as:section name="outro" soundSegment="outro">
#     <as:sub name="outropart1"> Hello outro part 1 </as:sub>
#     <as:sub name="outropart2"> Hello outro part 2 </as:sub>
#     <as:sub name="outropart3"> some extra text </as:sub>
# </as:section>
# """


# script = audiostack.Content.Script.create(scriptText=scriptText, scriptName="21b")
# print("response from creating script", script.response)
# scriptId = script.scriptId
# print(scriptId)
# create one tts resource

# tts = audiostack.Speech.TTS.Section.create(scriptItem=script, voice='sara', sectionToProduce="intro")#, useDictionary=True, useTextNormalizer=True)
# print(tts)
# tts.download()

# tts = audiostack.Speech.TTS.create(scriptItem=script, voice='sara')#, useDictionary=True, useTextNormalizer=True)
# print(tts)
# #print(tts.speechId)

# # now generate several different templates of this
# #mix = audiostack.Production.Mix.create(speechItem=speech, soundTemplate=template, exportSettings={"ttsTrack" : True})
# mix = audiostack.Production.Mix.create(speechItem=tts, soundTemplate="openup", exportSettings={"ttsTrack" : True}, timelineProperties={"fadeOut" : 3.0})
# print(mix)
# mix.download()

# # test mixing presets
# a = audiostack.Production.Mix.list_presets()
# print(a)

# # test list encoder and loudness presets
# a = audiostack.Delivery.Encoder.list_presets()
# print(a)

# # test wav encoding with spotify loudness
# encoded = audiostack.Delivery.Encoder.encode_mix(productionId='8f7bb5c2-c6fd-4a69-8e9f-34fd77eb4cf9', preset='wav', loudnessPreset="spotify")
# encoded.download(fileName="spotify")

# # print(audiostack.billing_session)



""" TEST SOUNDTEMPLATES_V3"""
# test sound
res = []
# try:
#     res = audiostack.Production.Sound.Template.create(templateName="test_2")
#     print(res)
# except Exception as e:
#     print(e)

# try:
#     res = audiostack.Production.Sound.Segment.create(templateName="test_2", soundSegmentName="intro", mediaId=1111)
#     print(res)
# except Exception as e:
#     print(e)

# try:
#     res = audiostack.Production.Sound.Template.delete(templateName="test_2")
#     print(res)
# except Exception as e:
#     print(e)

# try:
#     res = audiostack.Production.Sound.Parameter.get()
#     print(res)
# except Exception as e:
#     print(e)

try:
    res = audiostack.Production.Sound.get()
    print(res)
except Exception as e:
    print(e)


try:
    res = audiostack.Production.Sound.Template.list(moods="happy,sad")
    print(res)
except Exception as e:
    print(e)
