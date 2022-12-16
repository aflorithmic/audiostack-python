
import audiostack
import os

audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]


text = """

<<soundSegment::intro>>
<<sectionName::intro>>
What if we told you a story about the future of audio.  <<soundEffect::ding>>
A future in which audio can be created without the need for a  <<soundEffect::ding>> studio, or even much know how about audio.   <<soundEffect::ding>> Here at audiostack we have an entire eco system of possibilities
"""

script = audiostack.Content.Script.create(scriptText=text)
print(script)

tts = audiostack.Speech.TTS.create(scriptItem=script, voice="sara")
print(tts.response)


mix = audiostack.Production.Mix.create(speechItem=tts, soundTemplate="lifestylepodcast")
print(mix.response)

mix.download(fileName="error")
 