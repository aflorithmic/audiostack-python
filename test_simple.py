import audiostack
import os

audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]

scriptText = """
<<soundSegment::intro>><<sectionName::intro>> Hello <<soundSegment::main>> <<sectionName::main>> this is main <<soundSegment::outro>><<sectionName::outro>> goodbye
"""

script = audiostack.Content.Script.create(scriptText=scriptText)
print("response from creating script", script.response)
scriptId = script.scriptId

# create one tts resource
tts = audiostack.Speech.TTS.create(scriptItem=script, voice="sara")
print(tts.speechId)

# now generate several different templates of this

mix = audiostack.Production.Mix.create(speechItem=tts, soundTemplate="vinylhits")
print(mix)


encoded = audiostack.Delivery.Encoder.encode_mix(productionItem=mix, preset="mp3")
encoded.download(fileName="final")
