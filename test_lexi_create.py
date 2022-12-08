import audiostack
import os

audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]



word = audiostack.Speech.Diction.Custom.create_word("AFLR", "aflorithmic")
print(word)


word = audiostack.Speech.Diction.Custom.delete_word("AFLR", "aflorithmic")
print(word)
