import os
import audiostack
import json
import time

# DONT TEST THIS

#assert False, "sorry this is under construction"

audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]

start_time = time.time()
script = audiostack.Content.Script.create(scriptText="Happy birthday employee {{name}}. For you birthday you can have 3 drinks on us! Lucky you!")
print(script.response)

audience = {
    "name" : ["Sam", "Timo", "Peadar", "Bjorn", "Matt", "Lars", "Marcin", "Maria", "Hugo", "Liana", "Tim", "Thais", "Nikesh", "Davide", "Marti"]
}

r = audiostack.Orchestrator.Audioform.create_speech(audience=audience, scriptItem=script, voice="Sara")
print(r)

print("{:.4f}".format(time.time() - start_time))

tts_files = audiostack.Speech.TTS.list(scriptId=script.scriptId)
print(tts_files.response)

for tts in tts_files:
    print("getting", tts.speechId)
    # simple syntax, get TTS and then download
    item = audiostack.Speech.TTS.get(tts.speechId)
    print(item.response)
    item.download(autoName=True)
    



