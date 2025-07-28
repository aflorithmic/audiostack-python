import os
import random

import audiostack
from audiostack.production.sound import Sound

audiostack.api_base = os.environ.get("AUDIO_STACK_DEV_URL", "https://v2.api.audio")
audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]  # type: ignore

TEST_FILE_ID = ""


def test_list() -> None:
    sounds = Sound.Template.list()
    for s in sounds:
        assert isinstance(s, Sound.Template.Item)
    global TEST_FILE_ID
    TEST_FILE_ID = random.choice(seq=sounds.data["templates"])["soundTemplateId"]


def test_recommend() -> None:
    filters = [
        {"greaterThanOrEquals": {"duration": [300]}},
    ]
    x = 3
    force_apply_filters = False

    response = Sound.Template.recommend(
        soundTemplateId=TEST_FILE_ID,
        x=x,
        filters=filters,
        force_apply_filters=force_apply_filters,
    )
    assert response.status_code == 200
    assert len(response.data["soundTemplates"]) == x
