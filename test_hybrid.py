import audiostack
import os

audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]

media = audiostack.Content.Media.create(filePath="Timo.mp3")
print(media.mediaId)

scriptTxt = """
<<soundSegment::intro>><<sectionName::intro>> Hello Sam how are you? 
<<soundSegment::main>> <<sectionName::main>> This is main <<media::media1>>
<<soundSegment::outro>><<sectionName::outro>> goodbye
"""

scriptItem = audiostack.Content.Script.create(scriptText=scriptTxt)
print(scriptItem.response)
speechItem = audiostack.Speech.TTS.create(scriptItem=scriptItem, voice="Sara")
print(speechItem)
mixItem = audiostack.Production.Mix.create(speechItem=speechItem, soundTemplate="vinylhits", mediaFiles={"media1" : media.mediaId})
print(mixItem)
mixItem.download()
