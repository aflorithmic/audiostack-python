import audiostack
import os


"""
Hello! Welcome to the audiostack python SDK. 
"""

# make sure you change this to be your api key, or export it as AUDIO_STACK_DEV_KEY="<key>"
audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]

# lets personalise this audio asset for you so tel us your name
your_name = "Sam"

# put your friends names in here and we will demonstrate how our audio assets can scale
friends_names = ["Lars", "Marcin", "Maria"] 

# we have provided some default sound templates and a voice here for you.
sound_template = "cityechoes"
voice = "Sara"

scriptText = "Hello there! Your friend " + your_name + " has created a personalised audio asset for you {{friend|name}} using the new audiostack SDK. Goodbye!" 


script = audiostack.Content.Script.create(scriptText=scriptText)
print(script.message, script.scriptId)

tts = audiostack.Speech.TTS.create(scriptItem=script, voice=voice)
print(tts)
tts.download(autoName=True)

mix = audiostack.Production.Mix.create(speechItem=tts, soundTemplate=sound_template)
print(mix)

enc = audiostack.Delivery.Encoder.encode_mix(productionItem=mix, preset="mp3_low")
enc.download()


tts.delete()
print(tts)