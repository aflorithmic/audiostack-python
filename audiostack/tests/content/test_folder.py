import os

import audiostack
from audiostack.content.file import Folder

audiostack.api_base = os.environ.get("AUDIO_STACK_DEV_URL", "https://v2.api.audio")
audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]  # type: ignore

test_constants: dict = {}  #


def test_create() -> None:
    r = Folder.create(name="__PYTHON_TEST")
    test_constants["folder_id"] = r.data["folderId"]
    print(r)


def test_delete() -> None:
    Folder.delete(folder_id=test_constants["folder_id"])
