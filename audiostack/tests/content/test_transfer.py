import os

import audiostack
from audiostack.content.file import File

audiostack.api_base = os.environ.get("AUDIO_STACK_DEV_URL", "https://v2.api.audio")
audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]  # type: ignore

test_constants = {}  # type: dict


def test_transfer() -> None:
    script = audiostack.Content.Script.create(scriptText="hello sam")

    speech = audiostack.Speech.TTS.create(scriptItem=script, voice="sara")

    mix = audiostack.Production.Mix.create(speechItem=speech)
    print(mix)

    r = File.transfer(
        url=mix.data["files"][0]["url"], uploadPath="mymix.wav", tags=["a"]
    )
    print(r)

    delivery = audiostack.Delivery.Encoder.encode_mix(
        productionItem=mix, preset="mp3_very_high"
    )
    print(delivery, delivery.url)

    r2 = File.transfer(url=delivery.url, uploadPath="mymix.mp3", tags=["a"])
    print(r2)

    r.delete()
    r2.delete()
