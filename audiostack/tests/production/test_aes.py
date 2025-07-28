import os

import pytest

import audiostack
from audiostack.content.file import File

audiostack.api_base = os.environ.get("AUDIO_STACK_DEV_URL", "https://v2.api.audio")
audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]  # type: ignore


@pytest.mark.skip(
    reason="This test doesn't work with files v2",
)
def test_create() -> None:
    r = File.create(local_path="example.mp3", file_name="example.mp3")
    print("fileId: ", r.file_id)
    aesItem = audiostack.Production.Suite.evaluate(fileId=r.file_id)
    assert aesItem.status_code == 200, "BiG ERROR"
