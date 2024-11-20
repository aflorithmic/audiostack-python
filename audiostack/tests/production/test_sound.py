import os

import audiostack
from audiostack.production.sound import Sound

audiostack.api_base = os.environ.get("AUDIO_STACK_DEV_URL", "https://v2.api.audio")
audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]  # type: ignore


def test_list() -> None:
    sounds = Sound.Template.list()
    for s in sounds:
        assert isinstance(s, Sound.Template.Item)


def test_recommend() -> None:
    sound_template_id = "37bb15e6-15b2-4f46-af0f-559f0273cb6a"
    filters = [
        {"greaterThanOrEquals": {"duration": [300]}},
    ]
    x = 3
    force_apply_filters = False

    response = Sound.Template.recommend(
        soundTemplateId=sound_template_id,
        x=x,
        filters=filters,
        force_apply_filters=force_apply_filters,
    )
    assert response.status_code == 200
    assert len(response.data["soundTemplates"]) == x
