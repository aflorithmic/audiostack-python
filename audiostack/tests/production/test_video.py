import os

import audiostack
from audiostack.delivery.video import Video

audiostack.api_base = os.environ.get("AUDIO_STACK_DEV_URL", "https://v2.api.audio")
audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]  # type: ignore

test_constants = {}  # type: dict


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
