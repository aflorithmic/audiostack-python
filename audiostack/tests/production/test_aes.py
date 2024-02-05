import os
import audiostack

from audiostack.content.file import File

audiostack.api_base = os.environ.get("AUDIO_STACK_DEV_URL", "https://v2.api.audio")
audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]



def test_create():
    r = File.create(localPath="ttsTrack.mp3", uploadPath="ttsTrack.mp3", fileType="audio")
    print("fileId: ", r.fileId)
    aesItem = audiostack.Production.Suite.evaluate(fileId=r.fileId)
    assert aesItem.status_code==200, 'BiG ERROR'

