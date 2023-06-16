import audiostack
import os

audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]

res = audiostack.Content.Media.create(filePath="final.mp3")
print(res.response)


mediaFiles = audiostack.Content.Media.list()
for m in mediaFiles:
    #r = m.delete()
    print(m.mediaId, m.filename)
