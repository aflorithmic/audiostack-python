import audiostack
import os

audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]



word = audiostack.Speech.Diction.Custom.create_word(word="AFLR", replacement="phonemes", lang="de", specialization="voice_name", contentType="ipa")

scriptItem = audiostack.Content.Script.create(scriptText="hello AFLR")

# to preview the effect of the script processing pipleine
item = audiostack.Content.Script.get(scriptId=scriptItem.scriptId, previewWithVoice="voice_name")

speech = audiostack.Speech.TTS.create(scriptId=scriptItem.scriptId, useDictionary=True, useTextNormalizer=True, voice="voice_name")
speech.download()


print(word)


word = audiostack.Speech.Diction.Custom.delete_word("AFLR", "aflorithmic")
print(word)
