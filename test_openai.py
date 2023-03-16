import audiostack
import os

#audiostack.api_base = "https://staging-v2.api.audio"
audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]

scriptText = "Rephrase this for me: "

content = audiostack.Content.generate(scriptText, 200).data["content"]

print("response from creating script", content)


script = audiostack.Content.Script.create(scriptText=content)
tts = audiostack.Speech.TTS.create(scriptItem=script, voice="sara")
mix = audiostack.Production.Mix.create(speechItem=tts, soundTemplate="vinylhits")
encoded = audiostack.Delivery.Encoder.encode_mix(productionItem=mix, preset="mp3")
encoded.download(fileName="final")

