import os
from typing import Generator
from uuid import UUID

import pytest

import audiostack
from audiostack.files.file import File
from audiostack.folders.folder import Folder
from audiostack.tests.utils import create_test_file_name, create_test_folder_name

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

    resources: dict[str, list[str | None]] = {
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


@pytest.fixture
def test_file(cleanup_resources: dict) -> File.Item:
    """Fixture to create a test file for unit tests."""
    root_folder_id = Folder.get_root_folder_id()
    file = File.create(
        localPath="example.mp3",
        fileName=create_test_file_name() + ".mp3",
        folderId=UUID(root_folder_id),
    )
    cleanup_resources["file_ids"].append(file.fileId)
    return file


@pytest.fixture
def test_folder(cleanup_resources: dict) -> Folder.Item:
    """Fixture to create a test folder for unit tests."""
    folder = Folder.create(name=create_test_folder_name())
    cleanup_resources["folder_ids"].append(folder.folderId)
    return folder
