import os

import audiostack
from audiostack.delivery.video import Video

audiostack.api_base = os.environ.get("AUDIO_STACK_DEV_URL", "https://v2.api.audio")
audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]  # type: ignore

test_constants = {}  # type: dict


def test_create_from_production_and_image():
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


def test_create_from_production_and_video():
    script = audiostack.Content.Script.create(scriptText="hello lars")
    speech = audiostack.Speech.TTS.create(scriptItem=script, voice="sara")
    mix = audiostack.Production.Mix.create(speechItem=speech)
    videoFileId = "e655867d-c12f-42ad-a57e-466598ab84aa"
    mode = {"setting": "low"}
    format = "mp4"

    video = Video.create_from_production_and_video(
        productionItem=mix,
        videoFileId=videoFileId,
        public=True,
        format=format,
        mode=mode,
    )
    print(video)
    assert video.status_code == 200, "Video from production and video Failed"


def test_create_from_file_and_video():
    fileId = "11c7fcf7-d7cd-4c83-ba6b-a383a6d16a30"
    videoFileId = "e655867d-c12f-42ad-a57e-466598ab84aa"
    mode = {"setting": "low"}
    format = "mp4"

    video = Video.create_from_file_and_video(
        fileId=fileId, videoFileId=videoFileId, mode=mode, format=format, public=False
    )
    print(video)
    assert video.status_code == 200, "Video from file and video Failed"


def test_create_from_file_and_image():
    fileId = "11c7fcf7-d7cd-4c83-ba6b-a383a6d16a30"
    mode = {"setting": "default"}
    format = "mp4"

    video = Video.create_from_file_and_image(fileId=fileId, mode=mode, format=format)
    print(video)
    assert video.status_code == 200, "Video from file and image"
