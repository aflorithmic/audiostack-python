# TODO: User proper pytest fixtures
import os
import random
import string

import audiostack
from audiostack.content.file import Folder

audiostack.api_base = os.environ.get("AUDIO_STACK_DEV_URL", "https://v2.api.audio")
audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]  # type: ignore

test_constants: dict = {}  #


def create_test_folder_name() -> str:
    return "__PYTHON_TEST_" + "".join(
        random.choice(string.ascii_letters) for _ in range(10)
    )


def test_create() -> None:
    r = Folder.create(name=create_test_folder_name())
    test_constants["folder_id"] = r.folder_id
    print(r)


def test_get() -> None:
    r = Folder.get(folder_id=test_constants["folder_id"])
    print(r)


def test_delete() -> None:
    Folder.delete(folder_id=test_constants["folder_id"])
