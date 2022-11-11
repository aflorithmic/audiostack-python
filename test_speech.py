import json
import audiostack

audiostack.api_key = "0b1173a6420c4c028690b7beff39c0ad"


response, script = audiostack.Content.Script.create(scriptText="hello sam")
print("response from creating script", response)


scriptId = script.scriptId

for v in ["sara", "joanna", "conrad", "liam"]:
    r, item = audiostack.Speech.TTS.create(scriptItem=script, voice=v)
    print(r)


r, tts_files = audiostack.Speech.TTS.list(scriptId=scriptId)
for tts in tts_files:
    print("getting", tts.speechId)
    r, item = audiostack.Speech.TTS.get(tts.speechId)
    item.download(fileName=item.speechId)
    

#item.download(fileName="firstfile")
#  cx
# print("Cost for this session", audiostack.billing_session)

# r, item = audiostack.Production.create(...)
# print(r)

# item.encode(format="mp3")
# item.download(name="file1")

# #and for another.
# item.encode(format="wav16")
# item.download(name="file2")

# #vs

# r = audiostack.Production.create(...)

# r = audiostack.Deliver.encode(id= r["productionId"], format="mp3")
# r = audiostack.Deliver.download(id = r["enoderId"], name="file2")


