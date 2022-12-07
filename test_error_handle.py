import audiostack
import os

audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]


# create script item
item = audiostack.Content.Script.create(scriptText="hello sam", projectName="$%^&test")
print(item.response)


print("Cost for this session: ", audiostack.credits_used_in_this_session())