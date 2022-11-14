import audiostack
import os

audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]

script = audiostack.Content.Script.create(scriptText="hello sam")
print("response from creating script", script.response)


scriptId = script.scriptId

for v in ["sara", "joanna", "conrad", "liam"]:
    item = audiostack.Speech.TTS.create(scriptItem=script, voice=v)
    print(item.response)


tts_files = audiostack.Speech.TTS.list(scriptId=scriptId)
print(tts_files.response)
for tts in tts_files:
    print("getting", tts.speechId)
    item = audiostack.Speech.TTS.get(tts.speechId)
    item.download(fileName=item.speechId)


tts_files = audiostack.Speech.TTS.list(scriptId=scriptId)
print(tts_files.response)
for tts in tts_files:
    item = audiostack.Speech.TTS.get(tts.speechId)
    r = item.delete()
    print(r)

print("Cost for this session: ", audiostack.credits_used_in_this_session())