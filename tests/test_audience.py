# import sys
# sys.path.append("../")
import audiostack
import os

audiostack.api_base = "https://staging-v2.api.audio"
audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]

print(audiostack.Content.list_projects())

# scriptText = """
# <as:section name="intro" soundsegment="intro"> 
#     hello enjoy a coffee with <as:placeholder id="name">name</as:placeholder>
# </as:section>
# """

# script = audiostack.Content.Script.create(scriptText=scriptText)
# print("response from creating script", script.response)
# scriptId = script.scriptId

# # create one tts resource
# tts = audiostack.Speech.TTS.create(scriptItem=script, voice="sara", audience={"name" : "Sam"})
# print(tts.speechId)

# tts.download(fileName="name")