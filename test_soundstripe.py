import audiostack
import os

audiostack.api_key = "8b2984b2debb42b4979f22a10e77e83c"# os.environ["AUDIO_STACK_DEV_KEY"]


scriptText = """ hello everyone this is sound stripe working! we can add this to our API very easily I think."""

script = audiostack.Content.Script.create(scriptText=scriptText)
print("response from creating script", script.response)
scriptId = script.scriptId

# create one tts resource
tts = audiostack.Speech.TTS.create(scriptItem=script, voice="joanna")
print(tts.speechId)

# now generate several different templates of this

audiostack.Production.Sound.Template.generate(energy="low")

mix = audiostack.Production.Mix.create(speechItem=tts, soundTemplate="soundstripe")
print(mix)
#mix.download(fileName=st)

encoded = audiostack.Delivery.Encoder.encode_mix(productionItem=mix, preset="mp3")
encoded.download(fileName="epic")

