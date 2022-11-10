import audiostack

audiostack.api_key = "0b1173a6420c4c028690b7beff39c0ad"


response, item = audiostack.Content.Script.create(scriptText="hello sam")
print("response from creating script", response)

r, item = audiostack.Speech.TTS.create(scriptItem=item, voice="sara")
print(r)

item.download(fileName="firstfile")

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


