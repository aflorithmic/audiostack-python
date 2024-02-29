import os
import pytest
from unittest.mock import patch, Mock

import audiostack
from audiostack.helpers.request_types import RequestTypes

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


@patch("audiostack.content.recommend.RecommendTag.Item")
@patch("audiostack.content.recommend.RecommendTag.interface.send_request")
def test_RecommendTag_create(
    mock_send_request: Mock,
    mock_tag_item: Mock,
    text: str,
    category: str,
    tags: list,
    number_of_results: int,
):
    response = audiostack.Content.RecommendTag.create(
        text=text, category=category, tags=tags, number_of_results=number_of_results
    )

    payload = {
        "text": text,
        "category": category,
        "tags": tags,
        "number_of_results": number_of_results,
    }

    mock_send_request.assert_called_once_with(
        rtype=RequestTypes.POST, route="recommend/tag", json=payload
    )
    mock_tag_item.assert_called_once_with(mock_send_request.return_value)

    assert response == mock_tag_item.return_value


def test_integration_tag(
    text: str, category: str, tags: list, number_of_results: int
) -> None:
    item = audiostack.Content.RecommendTag.create(
        text=text, category=category, tags=tags, number_of_results=number_of_results
    )
    assert item.status_code == 200
    assert hasattr(item, "tags")


@patch("audiostack.content.recommend.RecommendTone.Item")
@patch("audiostack.content.recommend.RecommendTone.interface.send_request")
def test_RecommendTone_create(
    mock_send_request: Mock,
    mock_tone_item: Mock,
    text: str,
    category: str,
    tags: list,
    number_of_results: int,
):
    response = audiostack.Content.RecommendTone.create(
        text=text, number_of_results=number_of_results
    )

    payload = {"text": text, "number_of_results": number_of_results}

    mock_send_request.assert_called_once_with(
        rtype=RequestTypes.POST, route="recommend/tone", json=payload
    )
    mock_tone_item.assert_called_once_with(mock_send_request.return_value)

    assert response == mock_tone_item.return_value


def test_integration_tone(text: str, number_of_results: int) -> None:
    item = audiostack.Content.RecommendTone.create(
        text=text, number_of_results=number_of_results
    )
    assert item.status_code == 200
    assert hasattr(item, "tones")


@patch("audiostack.content.recommend.RecommendMood.Item")
@patch("audiostack.content.recommend.RecommendMood.interface.send_request")
def test_RecommendMood_create(
    mock_send_request: Mock,
    mock_mood_item: Mock,
    text: str,
    category: str,
    tags: list,
    number_of_results: int,
):
    response = audiostack.Content.RecommendMood.create(
        text=text, number_of_results=number_of_results
    )

    payload = {"text": text, "number_of_results": number_of_results}

    mock_send_request.assert_called_once_with(
        rtype=RequestTypes.POST, route="recommend/mood", json=payload
    )
    mock_mood_item.assert_called_once_with(mock_send_request.return_value)

    assert response == mock_mood_item.return_value


def test_integration_mood(text: str, number_of_results: int) -> None:
    item = audiostack.Content.RecommendMood.create(
        text=text, number_of_results=number_of_results
    )
    assert item.status_code == 200
    assert hasattr(item, "moods")
