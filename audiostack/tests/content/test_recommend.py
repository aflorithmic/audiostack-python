import os
import pytest

import audiostack

audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]

@pytest.fixture
def text():
    return "AudioStack’s technology seamlessly integrates into your product or workflow and cuts your audio production cycles to seconds while making your budgets go further."

@pytest.fixture
def category():
    return "my_custom_tags"

@pytest.fixture
def tags():
    return ["happy", "sad", "valuable"]

@pytest.fixture
def number_of_results(): 
    return 2

def test_integration_tag(text: str, category: str, tags: list, number_of_results: int) -> None:
    item = audiostack.Content.RecommendTag.post(text=text, category=category, tags=tags, number_of_results=number_of_results)
    assert item.status_code == 200

def test_integration_tone(text: str, number_of_results: int) -> None:
    item = audiostack.Content.RecommendTone.post(text=text, number_of_results=number_of_results)
    assert item.status_code == 200

def test_integration_mood(text: str, number_of_results: int) -> None:
    item = audiostack.Content.RecommendMood.post(text=text, number_of_results=number_of_results)
    assert item.status_code == 200