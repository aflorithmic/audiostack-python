import os

import audiostack
from audiostack.content.file import File

audiostack.api_base = os.environ.get("AUDIO_STACK_DEV_URL", "https://v2.api.audio")
audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]  # type: ignore

test_constants = {}


def test_create() -> None:
    r = File.create(local_path="example.mp3", file_name="test.mp3")
    test_constants["fileId"] = r.file_id
    test_constants["fileName"] = r.file_name
    print(r)


def test_get() -> None:
    r = File.get(file_id=test_constants["fileId"])
    print(r)


def test_delete() -> None:
    r = File.delete(file_id=test_constants["fileId"])
    print(r)
