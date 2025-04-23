import os

import pytest

import audiostack
from audiostack.content.file import File, Folder

audiostack.api_base = os.environ.get("AUDIO_STACK_DEV_URL", "https://v2.api.audio")
audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]  # type: ignore

test_constants = {}


def test_create() -> None:
    r = File.create(local_path="example.mp3", file_name="test")
    test_constants["fileId"] = r.file_id
    test_constants["fileName"] = r.file_name
    print(r)


def test_get() -> None:
    r = File.get(test_constants["fileId"])
    print(r)


def test_modify() -> None:
    r = File.modify(
        file_id=test_constants["fileId"], file_name=test_constants["fileName"]
    )
    print(r)


def test_delete() -> None:
    r = File.delete(
        test_constants["fileId"], Folder.get_root().current_path_chain["folderId"]
    )
    print(r)
