import os

import pytest

import audiostack
from audiostack.files.file import File

audiostack.api_base = os.environ.get("AUDIO_STACK_DEV_URL", "https://v2.api.audio")
audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]  # type: ignore


@pytest.mark.skip(
    reason="This test doesn't work with files v2",
)
def test_create() -> None:
    r = File.create(
        localPath="example.mp3", uploadPath="example.mp3", fileName="example.mp3"
    )
    print("fileId: ", r.fileId)
    aesItem = audiostack.Production.Suite.evaluate(fileId=r.fileId)
    assert aesItem.status_code == 200, "BiG ERROR"
