import os

import audiostack
from audiostack.delivery.video import Video

audiostack.api_base = os.environ.get("AUDIO_STACK_DEV_URL", "https://v2.api.audio")
audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]  # type: ignore

test_constants = {}  # type: dict

if "staging" in audiostack.api_base:
    FILE_IDS = {
        "video": "e655867d-c12f-42ad-a57e-466598ab84aa",
        "audio": "11c7fcf7-d7cd-4c83-ba6b-a383a6d16a30",
    }
else:
    FILE_IDS = {
        "video": "87c3399e-4c92-4bb5-8e95-e39564afc09a",
        "audio": "04200ee6-d74f-4f46-adbd-90c7453beede",
    }


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


def test_create_from_production_and_video() -> None:
    script = audiostack.Content.Script.create(scriptText="hello lars")
    speech = audiostack.Speech.TTS.create(scriptItem=script, voice="sara")
    mix = audiostack.Production.Mix.create(speechItem=speech)

    videoFileId = FILE_IDS["video"]
    mode = {"setting": "low"}

    video = Video.create_from_production_and_video(
        productionItem=mix,
        videoFileId=videoFileId,
        public=True,
        mode=mode,
    )
    print(video)
    assert video.status_code == 200, "Video from production and video Failed"


def test_create_from_file_and_video() -> None:
    fileId = FILE_IDS["audio"]
    videoFileId = FILE_IDS["video"]
    mode = {"setting": "low"}

    video = Video.create_from_file_and_video(
        fileId=fileId, videoFileId=videoFileId, mode=mode
    )
    print(video)
    assert video.status_code == 200, "Video from file and video Failed"


def test_create_from_file_and_image() -> None:
    fileId = FILE_IDS["audio"]

    video = Video.create_from_file_and_image(fileId=fileId)
    print(video)
    assert video.status_code == 200, "Video from file and image"
