import os
from typing import Generator
from uuid import UUID

import pytest

import audiostack

audiostack.api_base = os.environ.get(
    "AUDIO_STACK_DEV_URL", "https://staging-v2.api.audio"
)
audiostack.api_key = os.environ.get("AUDIO_STACK_DEV_KEY", None)  # type: ignore


@pytest.fixture
def script_item() -> Generator[audiostack.Content.Script.Item, None, None]:
    script = audiostack.Content.Script.create(scriptText="hello sam")
    yield script
    audiostack.Content.Script.delete(scriptId=script.scriptId)


@pytest.fixture
def speech_item(
    script_item: audiostack.Content.Script.Item,
) -> Generator[audiostack.Speech.TTS.Item, None, None]:
    tts = audiostack.Speech.TTS.create(
        scriptId=script_item.scriptId,
        voice="isaac",
    )
    yield tts
    audiostack.Speech.TTS.delete(speechId=tts.speechId)


@pytest.fixture
def cleanup_resources() -> Generator[dict, None, None]:
    """Fixture to track and clean up test resources for files/folders tests."""
    from audiostack.files.file import File
    from audiostack.folders.folder import Folder

    resources = {
        "file_ids": [],
        "folder_ids": [],
    }

    yield resources

    # Cleanup: delete all tracked resources
    for file_id in resources["file_ids"]:
        try:
            File.delete(fileId=UUID(file_id))
        except Exception:
            pass

    for folder_id in resources["folder_ids"]:
        try:
            Folder.delete(folderId=UUID(folder_id))
        except Exception:
            pass

