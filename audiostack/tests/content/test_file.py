import os

import pytest

import audiostack
from audiostack.content.file import File

audiostack.api_base = os.environ.get("AUDIO_STACK_DEV_URL", "https://v2.api.audio")
audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]  # type: ignore

test_constants = {}


def test_create() -> None:
    r = File.create(localPath="example.mp3", uploadPath="example.mp3", fileType="audio")
    test_constants["fileId"] = r.fileId
    print(r)


def test_get() -> None:
    r = File.get(test_constants["fileId"])
    print(r)


def test_modify() -> None:
    r = File.modify(fileId=test_constants["fileId"], category="test")
    print(r)


@pytest.mark.skip(reason="Raises KeyError: 'items'")
def test_search() -> None:
    files = File.search()
    for f in files:
        print(f)

    files = File.search(source="pythonSDK")
    for f in files:
        print(f)


def test_delete() -> None:
    r = File.get(test_constants["fileId"])
    r2 = r.delete()
    print(r2)


def test_create_2() -> None:
    r = File.create(
        localPath="example.mp3",
        uploadPath="example.mp3",
        fileType="audio",
        category="sounds",
        tags=["a", "b"],
        metadata={"hello": "world"},
    )
    test_constants["fileId"] = r.fileId
    print(r)
    r.delete()
