import os

import audiostack
from audiostack.production.sound import Sound

audiostack.api_base = os.environ.get("AUDIO_STACK_DEV_URL", "https://v2.api.audio")
audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]  # type: ignore


def test_list() -> None:
    sounds = Sound.Template.list()
    for s in sounds:
        assert isinstance(s, Sound.Template.Item)
