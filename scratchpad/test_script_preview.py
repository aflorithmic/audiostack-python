import audiostack
import os

audiostack.api_key = "0b1173a6420c4c028690b7beff39hdik"# os.environ["AUDIO_STACK_DEV_KEY"]

# create script item
item = audiostack.Content.Script.create(scriptText="hello sam lets check the <!preview>", projectName="__test")
#print(item.response)

s = audiostack.Content.Script.get(item.scriptId, previewWithVoice="sara")
print(s.response)
