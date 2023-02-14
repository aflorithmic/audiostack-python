import audiostack
import os

audiostack.api_base = "https://staging-v2.api.audio"
audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]

scriptText = """
<as:section name="intro" soundsegment="intro"> hello this is the new script syntax </as:section>
<as:section name="main" soundsegment="main"> This uses regular H T M L syntax and replaces our old script formatting </as:section>
<as:section name="outro" soundsegment="outro"> this massively improves usability, aids with learnability and should improve adoption </as:section>
"""

script = audiostack.Content.Script.create(scriptText=scriptText, syntax="v2")
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
