import os

import audiostack
from audiostack.content.file import File

audiostack.api_base = os.environ.get("AUDIO_STACK_DEV_URL", "https://v2.api.audio")
audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]  # type: ignore

test_constants = {}


def test_create() -> None:
    r = File.create(localPath="example.mp3", uploadPath="test.mp3")
    test_constants["fileId"] = r.fileId
    test_constants["fileName"] = r.fileName
    print(r)


def test_get() -> None:
    r = File.get(fileId=test_constants["fileId"])
    print(r)


def test_delete() -> None:
    r = File.delete(fileId=test_constants["fileId"])
    print(r)
