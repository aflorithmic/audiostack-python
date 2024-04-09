import audiostack
import os



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


mix = audiostack.Production.Mix.create(speechItem=tts, masteringPreset="radio", soundTemplate="hotwheels")

#delivery

video = audiostack.Delivery.Video.create(
  productionItem=mix,
  public=True,
)

file_name = f'video-{voice_name}'
video.download(fileName=file_name)
print(video)

print()