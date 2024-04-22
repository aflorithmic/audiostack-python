import os
import audiostack

from audiostack.delivery.video import Video

audiostack.api_base = os.environ.get("AUDIO_STACK_DEV_URL", "https://v2.api.audio")
audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]

test_constants = {}


def test_video():
    script = audiostack.Content.Script.create(scriptText="hello sam")

    speech = audiostack.Speech.TTS.create(scriptItem=script, voice="sara")

    mix = audiostack.Production.Mix.create(speechItem=speech)
    print(mix)
        
    video = audiostack.Delivery.Video.create(
        productionItem=mix,
        public=True,
    )
    print(video)