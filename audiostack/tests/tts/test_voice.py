import os
import audiostack

from audiostack.speech.voice import Voice

audiostack.api_base = os.environ.get("AUDIO_STACK_DEV_URL]", "https://v2.api.audio")
audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]



def test_list():
    voices = Voice.list()
    for v in voices:
        assert isinstance(v, Voice.Item)
        assert v.provider
        assert v.alias
        assert v.data

def test_parmaters():
    r = Voice.Parameter.get()
    assert r