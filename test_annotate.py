import audiostack
import os

audiostack.api_base = "https://staging-v2.api.audio"
audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]


scriptText = """
    <as:section name="intro" soundsegment="intro">
    hello this is a test file for annotate, let's get timestamps for each word said in this speech file
    </as:section>

"""

script = audiostack.Content.Script.create(scriptText=scriptText, scriptName="test")

tts = audiostack.Speech.TTS.create(scriptItem=script, voice="joanna")

tts = audiostack.Speech.TTS.annotate(speechId=tts.speechId)
tts.download()
