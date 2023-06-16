import audiostack
import os

audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]


response = audiostack.Content.Script.list(projectName="__test")
script_list = response.items
for script_item in script_list:
    print(script_item.get("scriptId"))

print("Cost for this session: ", audiostack.credits_used_in_this_session())