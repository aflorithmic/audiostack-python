import os

import audiostack
from audiostack.delivery.video import Video

audiostack.api_base = os.environ.get("AUDIO_STACK_DEV_URL", "https://v2.api.audio")
audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]  # type: ignore

test_constants = {}  # type: dict
from typing import Generator
from uuid import uuid4

import pytest


@pytest.fixture(scope="module")
def _get_audio_file_id(request: pytest.FixtureRequest) -> Generator:
    r = audiostack.Content.File.create(
        localPath="audiostack/tests/fixtures/audio.wav",
        uploadPath=f"sdk_unit_tests_{str(uuid4())}.wav",
        fileType="audio",
    )
    r = audiostack.Content.File.get(fileId=r.fileId)
    yield r.fileId

    # Register the finalizer to delete the file at the end of the session
    def teardown() -> None:
        audiostack.Content.File.delete(fileId=r.fileId)

    request.addfinalizer(teardown)


@pytest.fixture(scope="module")
def _get_video_file_id(request: pytest.FixtureRequest) -> Generator:
    r = audiostack.Content.File.create(
        localPath="audiostack/tests/fixtures/video.mp4",
        uploadPath=f"sdk_unit_tests_{str(uuid4())}.mp4",
        fileType="video",
    )
    r = audiostack.Content.File.get(fileId=r.fileId)
    yield r.fileId

    # Register the finalizer to delete the file at the end of the session
    def teardown() -> None:
        audiostack.Content.File.delete(fileId=r.fileId)

    request.addfinalizer(teardown)


def test_create_from_production_and_image() -> None:
    script = audiostack.Content.Script.create(scriptText="hello sam")
    speech = audiostack.Speech.TTS.create(scriptItem=script, voice="sara")
    mix = audiostack.Production.Mix.create(speechItem=speech)
    print(mix)

    video = Video.create_from_production_and_image(
        productionItem=mix,
        public=True,
    )
    print(video)
    assert video.status_code == 200, "Video from production and image Failed"


def test_create_from_production_and_video(_get_video_file_id: str) -> None:
    script = audiostack.Content.Script.create(scriptText="Hello, how are you?")
    speech = audiostack.Speech.TTS.create(scriptItem=script, voice="sara")
    mix = audiostack.Production.Mix.create(speechItem=speech)

    mode = {"setting": "low"}
    video = Video.create_from_production_and_video(
        productionItem=mix,
        videoFileId=_get_video_file_id,
        public=True,
        mode=mode,
    )
    print(video)
    assert video.status_code == 200, "Video from production and video Failed"


def test_create_from_file_and_video(
    _get_audio_file_id: str, _get_video_file_id: str
) -> None:
    mode = {"setting": "low"}

    video = Video.create_from_file_and_video(
        fileId=_get_audio_file_id, videoFileId=_get_video_file_id, mode=mode
    )
    print(video)
    assert video.status_code == 200, "Video from file and video Failed"


def test_create_from_file_and_image(_get_audio_file_id: str) -> None:

    video = Video.create_from_file_and_image(fileId=_get_audio_file_id)
    print(video)
    assert video.status_code == 200, "Video from file and image"
