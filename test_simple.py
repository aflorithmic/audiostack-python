import audiostack
import os

#audiostack.api_base = "https://staging-v2.api.audio"
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


script = audiostack.Content.Script.create(scriptText=scriptText, scriptName="21b")
print("response from creating script", script.response)
scriptId = script.scriptId
print(scriptId)
# create one tts resource

tts = audiostack.Speech.TTS.Section.create(scriptItem=script, voice='sara', sectionToProduce="intro")#, useDictionary=True, useTextNormalizer=True)
print(tts)
tts.download()

# tts = audiostack.Speech.TTS.create(scriptItem=script, voice='sara')#, useDictionary=True, useTextNormalizer=True)
# print(tts)
# #print(tts.speechId)

# # now generate several different templates of this
# #mix = audiostack.Production.Mix.create(speechItem=speech, soundTemplate=template, exportSettings={"ttsTrack" : True})
# mix = audiostack.Production.Mix.create(speechItem=tts, soundTemplate="openup", exportSettings={"ttsTrack" : True}, timelineProperties={"fadeOut" : 3.0})
# print(mix)
# mix.download()

# # encoded = audiostack.Delivery.Encoder.encode_mix(productionItem=mix, preset="mp3")
# # encoded.download(fileName="final")

# # print(audiostack.billing_session)