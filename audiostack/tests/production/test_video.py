import audiostack
import os

# audiostack.api_key = "2ca962ca-6b56-478d-b726-23aec98cae65"
# audiostack.api_base = "https://v2.api.audio"

audiostack.api_base = "https://staging-v2.api.audio"
audiostack.api_key = "0b1173a6420c4c028690b7beff39hdik" # fill up


# Create a script
scriptText = """
Right now, get four thousand five hundred dollars cash allowance on the purchase of virtually ALL twenty twenty four Ram fifteen hundred trucks.
"""
voice_name="isaac"

script = audiostack.Content.Script.create(
  scriptText=scriptText,
  projectName="Demos",
)

#speech
tts = audiostack.Speech.TTS.create(
  scriptItem=script,
  voice=voice_name,
  speed=1.00,
  )


mix = audiostack.Production.Mix.create(speechItem=tts, masteringPreset="radio", soundTemplate="lofi")

#delivery

video = audiostack.Delivery.Video.create_video(
  productionItem=mix,
  public=True,
)

file_name = f'video-{voice_name}'
video.download(fileName=file_name)
print(video)

print()