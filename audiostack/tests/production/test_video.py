import os
from typing import Generator
from uuid import uuid4

import pytest

import audiostack
from audiostack.delivery.video import Video

audiostack.api_base = os.environ.get("AUDIO_STACK_DEV_URL", "https://v2.api.audio")
audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]  # type: ignore

test_constants = {}  # type: dict


@pytest.fixture(scope="module")
def _get_audio_file_id() -> Generator:
    r = audiostack.Content.File.create(
        local_path="audiostack/tests/fixtures/audio.wav",
        file_name=f"sdk_unit_tests_{str(uuid4())}.wav",
    )
    r = audiostack.Content.File.get(file_id=r.file_id)
    yield r.file_id

    audiostack.Content.File.delete(file_id=r.file_id)


@pytest.fixture(scope="module")
def _get_video_file_id() -> Generator:
    r = audiostack.Content.File.create(
        local_path="audiostack/tests/fixtures/video.mp4",
        file_name=f"sdk_unit_tests_{str(uuid4())}.mp4",
    )
    print("my file id", r.file_id)
    yield r.file_id
    # audiostack.Content.File.delete(file_id=r.file_id)


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


@pytest.mark.skip(
    reason="This doesn't work in files v2",
)
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


@pytest.mark.skip(
    reason="This doesn't work in files v2",
)
def test_create_from_file_and_video(
    _get_audio_file_id: str, _get_video_file_id: str
) -> None:
    mode = {"setting": "low"}

    video = Video.create_from_file_and_video(
        fileId=_get_audio_file_id, videoFileId=_get_video_file_id, mode=mode
    )
    print(video)
    assert video.status_code == 200, "Video from file and video Failed"


@pytest.mark.skip(
    reason="This doesn't work in files v2",
)
def test_create_from_file_and_image(_get_audio_file_id: str) -> None:
    video = Video.create_from_file_and_image(fileId=_get_audio_file_id)
    print(video)
    assert video.status_code == 200, "Video from file and image"
