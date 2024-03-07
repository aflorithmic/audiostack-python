import os
import audiostack
import pytest 

from audiostack.content.file import File

audiostack.api_base = os.environ.get("AUDIO_STACK_DEV_URL", "https://v2.api.audio")
audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]



def test_separate():
    r = File.create(localPath="ad_with_music_soundeffects.wav", uploadPath="ad_with_music_soundeffects.wav", fileType="audio")
    sepItem = audiostack.Production.Suite.SourceSeparation.separate(fileId=r.fileId)
    assert sepItem.status_code==200

