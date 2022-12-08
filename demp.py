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
friends_names = ["Timo", "Matt", "Maria"] 

# we have provided some default sound templates and a voice here for you.
sound_template = "cityechoes"
voice = "Sara"

scriptText = "Hello there! Your friend " + your_name + " has created a personalised audio asset for you {{friend|name}} using the new audiostack SDK. Goodbye!" 

script = audiostack.Content.Script.create(scriptText=scriptText)

for friend in friends_names:
    tts = audiostack.Speech.TTS.create(scriptItem=script, voice="Sara", audience={"friend" : friend})
    print(tts.message)

    mix = audiostack.Production.Mix.create(speechItem=tts, soundTemplate=sound_template)
    print(mix.message)

    encoder = audiostack.Delivery.Encoder.encode_mix(productionItem=mix, preset="mp3", public=True)
    print(encoder.message)

    encoder.download(fileName=friend)
    print("Personalised audio asset for ", friend, "created. Audio asset download, but use this url ", encoder.url, " to share with friends")

print("Cost for this session: ", audiostack.credits_used_in_this_session())