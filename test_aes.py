import audiostack
import os

audiostack.api_base = "https://staging-v2.api.audio"
audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]


file = audiostack.Content.File.create(localPath="input.wav", uploadPath="tests_for_aes/hey_test.wav", fileType="audio", category="audio", tags=["voice"])
print(file.fileId)

aesItem = audiostack.Production.Suite.evaluate(fileId=file.fileId)

scores = aesItem.data.get("scores")
values = aesItem.data.get("values")
transcript = aesItem.data.get("transcript")

print(aesItem)
pass
