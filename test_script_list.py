import audiostack
import os

audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]


response, script_list = audiostack.Content.Script.list(projectName="__test")

for script_item in script_list:
    print(script_item.scriptId)

print("Cost for this session: ", audiostack.credits_used_in_this_session())