import os

import audiostack
from audiostack.content.file import Folder

audiostack.api_base = os.environ.get("AUDIO_STACK_DEV_URL", "https://v2.api.audio")
audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]  # type: ignore

test_constants: dict = {}  #


def test_list() -> None:
    r = Folder.list(folder="")
    print(r)
    for fol in r.folders:
        print(fol)
    for fi in r.files:
        print(fi)


def test_create() -> None:
    r = Folder.delete(folder="__PYTHON_TEST", delete_files=True)
    r = Folder.create(name="__PYTHON_TEST")  # type: ignore
    print(r)


def test_delete() -> None:
    Folder.delete(folder="__PYTHON_TEST", delete_files=True)
