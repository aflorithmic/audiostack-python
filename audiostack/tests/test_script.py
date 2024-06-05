import os

import audiostack
from audiostack.content.script import Script

audiostack.api_base = os.environ.get("AUDIO_STACK_DEV_URL", "https://v2.api.audio")
audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]  # type: ignore

SCRIPT_ID = ""


def test_create() -> None:
    script_item = Script.create(
        scriptText="hello sam",
        projectName="sdk_test",
        moduleName="sdk_test",
        scriptName="sdk_1",
    )
    global SCRIPT_ID
    SCRIPT_ID = script_item.scriptId


def test_get() -> None:
    script_item = Script.get(scriptId=SCRIPT_ID)
    assert script_item


def test_update() -> None:
    Script.update(scriptId=SCRIPT_ID, scriptText="blah blah")


def test_preview() -> None:
    script_item = Script.get(scriptId=SCRIPT_ID, previewWithVoice="sara")
    assert script_item


def test_delete() -> None:
    Script.delete(scriptId=SCRIPT_ID)


def test_inbuilts() -> None:
    script_item = Script.create(
        scriptText="hello sam",
        projectName="sdk_test",
        moduleName="sdk_test",
        scriptName="sdk_1",
    )
    script_item.update(scriptText="this is an update")
    script_item.delete()


def test_list() -> None:
    items = Script.list()
    for i in items:
        assert isinstance(i, Script.Item)
        assert i.scriptId
