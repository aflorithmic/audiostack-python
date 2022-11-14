import json
import audiostack

audiostack.api_key = "0b1173a6420c4c028690b7beff39c0ad"


scriptText = "<<sectionName::intro>> Hello <<sectionName::main>> this is main <<sectionName::outro>> goodbye"


response, script = audiostack.Content.Script.create(scriptText=scriptText)
print("response from creating script", response)


r, tts = audiostack.Speech.TTS.create(scriptItem=script, voice="joanna")
print(tts.speechId)

r, mix = audiostack.Production.Mix.create(speechItem=tts, soundTemplate="vinylhits")
print(r)


r, encoded = audiostack.Delivery.Encoder.encode_mix(productionItem=mix, prest="mp3")
print(r)

encoded.download()



#mix.download(fileName="hellotest")


# # mix.encode(format="mp3_low")
# r = mix.encode(preset="mp3_high")
# print(r)
# r = mix.download(fileName="hellotest")
# print(r)