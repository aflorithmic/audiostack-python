import audiostack
import os

audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]

voice_params = audiostack.Speech.Voice.Parameter.get()
print("Parameters for voices = ", voice_params)

voices = audiostack.Speech.Voice.list()
for v in voices:
    print(v.alias)


print("Cost for this session: ", audiostack.credits_used_in_this_session())