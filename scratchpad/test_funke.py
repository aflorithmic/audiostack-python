import audiostack
import os

audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]
audiostack.api_base = "https://staging-v2.api.audio"

scriptText = """
<as:section name="section1"> Hello world </as:section>
<as:section name="section2"> hello section 2 </as:section>
"""

"3c0106fa-10d2-49df-a788-6e749ef25300"

script = audiostack.Content.Script.create(scriptText="hello sam this is a realy long script. hello sam this is a realy long script. hello sam this is a realy long script. hello sam this is a realy long script. hello sam this is a realy long script")
print("response from creating script", script.response)

# store scriptId for later
scriptId = script.scriptId

# do 4 requests - 1 for each voice :) 
for v in ["sara", "joanna", "conrad", "liam"]:
    item = audiostack.Speech.TTS.create(scriptItem=script, voice=v)
    print(item.response)

# now lets get our files with the list method
tts_files = audiostack.Speech.TTS.list(scriptId=scriptId)
print(tts_files.response)

for tts in tts_files:
    print("getting", tts.speechId)
    # simple syntax, get TTS and then download
    item = audiostack.Speech.TTS.get(tts.speechId)
    item.download(fileName=item.speechId)


# lets now list again
tts_files = audiostack.Speech.TTS.list(scriptId=scriptId)
print(tts_files.response)

for tts in tts_files:
    # and delete out files (not needed anymore)
    item = audiostack.Speech.TTS.get(tts.speechId)
    r = item.delete()
    print(r)

print("Cost for this session: ", audiostack.credits_used_in_this_session())