import audiostack
import os

audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]
#audiostack.api_base = "https://staging-v2.api.audio"


scriptText = """
<as:section name="intro" soundsegment="intro"> 
    hello this is the new script syntax 
</as:section>
<as:section name="main">
    This uses regular H T M L syntax and replaces our old script formatting 
</as:section>
<as:section name="outro" soundsegment="outro"> 
    This massively improves usability, aids with learnability and should improve adoption 
</as:section>"""

script = audiostack.Content.Script.create(scriptText=scriptText)
print("response from creating script", script.response)
scriptId = script.scriptId

# create one tts resource
tts = audiostack.Speech.TTS.create(scriptItem=script, voice="joanna")
print(tts.speechId)

# now generate several different templates of this
for st in ["jakarta"]:#, "openup", "hotwheels", "whatstillremains"]:#  "lifestylepodcast", "cityechoes"]:
    print("Mixing and encoding a preview of", st)
    mix = audiostack.Production.Mix.create(speechItem=tts, soundTemplate=st, exportSettings={"ttsTrack" : True})
    mix.download()

    encoded = audiostack.Delivery.Encoder.encode_mix(productionItem=mix, preset="mp3")
    encoded.download(fileName=st)

# lets list what we created and deleted it 
mix_files = audiostack.Production.Mix.list(scriptId=scriptId)
print(mix_files.response)
for mix in mix_files:
    item = audiostack.Production.Mix.get(mix.productionId)  
    r = item.delete()
    print(r)

print("Cost for this session: ", audiostack.credits_used_in_this_session())
