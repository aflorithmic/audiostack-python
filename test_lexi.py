import audiostack
import os

audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]

dicts = audiostack.Speech.Diction.list()
print("Public dicts = ", dicts.data)
print("Public dicts = ", dicts)

# voices = audiostack.Speech.Voice.list()
# for v in voices:
#     print(v.alias)


# print("Cost for this session: ", audiostack.credits_used_in_this_session())