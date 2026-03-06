from typing import Dict
from unittest.mock import MagicMock, patch

import pytest

from audiostack.creator import Story

# ============================================================================
# STORY.ITEM TESTS
# ============================================================================


def test_post_story_response(post_story_good_response: Dict) -> None:
    item = Story.Item(post_story_good_response)
    assert item.story_id == post_story_good_response.get("data").get("storyId")
    assert item.story_result == {}
    assert item.audioforms == []
    assert item._errors == ""


def test_post_story_no_storyid() -> None:
    mock_response = {
        "metadata": {
            "requestId": "request_id_5dfee7c2-549d-4c84-8f9f-be980cc0a304",
            "version": "123",
            "creditsUsed": 0.0,
            "creditsRemaining": 0.0,
        },
        "warnings": [],
        "message": "Story successfully created",
        "data": {},
    }
    with pytest.raises(Exception):
        Story.Item(mock_response)


def test_get_story_response(get_story_good_response: Dict) -> None:
    item = Story.Item(get_story_good_response)
    assert item.story_id == get_story_good_response.get("data").get("storyId")
    assert item.story_build_status_code == 200
    assert item.story_result == get_story_good_response.get("data").get("storyResult")
    assert item.audioforms == get_story_good_response.get("data").get("audioforms")
    assert item.is_success is True


def test_get_story_failed_build() -> None:
    mock_response = {
        "metadata": {
            "requestId": "request_id_367e6a21-0ffc-4b39-aaea-8381fab60d2a",
            "version": "123",
            "creditsUsed": 0.0,
            "creditsRemaining": 0.0,
        },
        "warnings": [],
        "message": "Build successfully retreived",
        "data": {
            "statusCode": 500,
            "message": "Failed to generate story",
            "storyId": "abc",
        },
    }
    item = Story.Item(mock_response)
    assert item.story_id == "abc"
    assert item.story_build_status_code == 500
    assert item.audioforms == []
    assert item._errors == "Failed to generate story"
    assert item.is_success is False


# ============================================================================
# STORY.CREATE TESTS
# ============================================================================


@patch("audiostack.creator.story.Story.interface.send_request")
def test_create_story(
    mock_send: MagicMock, correct_story_sample: Dict, post_story_good_response: Dict
) -> None:
    mock_send.return_value = post_story_good_response
    item = Story.create(story=correct_story_sample)
    mock_send.assert_called_once_with(
        rtype="POST", route="story", json={"story": correct_story_sample}
    )
    assert item.story_id == post_story_good_response.get("data").get("storyId")
    assert item.story_build_status_code is None
    assert item.audioforms == []
    assert item.story_result == {}
    assert item._errors == ""


def test_create_not_dict() -> None:
    story = "hello engineer, hope you're having a good day"
    with pytest.raises(Exception):
        Story.create(story=story)  # type: ignore


def test_create_no_story() -> None:
    with pytest.raises(Exception):
        Story.create()  # type: ignore


@patch("audiostack.creator.story.Story.interface.send_request")
def test_create_raises_on_400(mock_send: MagicMock, correct_story_sample: Dict) -> None:
    mock_send.side_effect = Exception("Validation failed - invalid story config")
    with pytest.raises(Exception) as exc_info:
        Story.create(story=correct_story_sample)
    assert "Validation failed" in str(exc_info.value)
    mock_send.assert_called_once_with(
        rtype="POST", route="story", json={"story": correct_story_sample}
    )


@patch("audiostack.creator.story.Story.interface.send_request")
def test_create_raises_on_500(mock_send: MagicMock, correct_story_sample: Dict) -> None:
    mock_send.side_effect = Exception("Internal server error - aborting")
    with pytest.raises(Exception) as exc_info:
        Story.create(story=correct_story_sample)
    assert str(exc_info.value) == "Internal server error - aborting"
    mock_send.assert_called_once_with(
        rtype="POST", route="story", json={"story": correct_story_sample}
    )


# ============================================================================
# STORY.GET TESTS
# ============================================================================


@patch("audiostack.creator.story.Story.interface.send_request")
def test_get_story(mock_send: MagicMock, get_story_good_response: Dict) -> None:
    mock_send.return_value = get_story_good_response
    item = Story.get(story_id="4550fde5-4c63-4fd0-853f-148010cd6278")
    mock_send.assert_called_once_with(
        rtype="GET",
        route="story",
        path_parameters="4550fde5-4c63-4fd0-853f-148010cd6278",
    )
    assert item.story_id == get_story_good_response.get("data").get("storyId")
    assert item.story_build_status_code == 200
    assert item.is_success is True


@patch("audiostack.creator.story.Story.interface.send_request")
def test_get_polling(mock_send: MagicMock) -> None:
    mock_send.side_effect = [
        {"statusCode": 202},
        {"statusCode": 202},
        {"statusCode": 202},
        {"statusCode": 200, "data": {"storyId": "test", "statusCode": 200}},
    ]

    with patch("time.sleep", return_value=None):
        result = Story.get("test")
    assert result.is_success is True
    assert mock_send.call_count == 4


@patch("audiostack.creator.story.Story.interface.send_request")
def test_get_timeout(mock_send: MagicMock) -> None:
    mock_send.return_value = {"statusCode": 202}

    with patch("time.sleep", return_value=None):
        with pytest.raises(TimeoutError) as e:
            Story.get("test", timeoutThreshold=1)
    assert "Story polling timed out" in str(e.value)
    assert "test" in str(e.value)


@patch("audiostack.creator.story.Story.interface.send_request")
def test_get_raises_on_400(mock_send: MagicMock) -> None:
    mock_send.side_effect = Exception("Validation failed - invalid story config")
    with pytest.raises(Exception) as exc_info:
        Story.get("test")
    mock_send.assert_called_once_with(
        rtype="GET", route="story", path_parameters="test"
    )
    assert str(exc_info.value) == "Validation failed - invalid story config"


@patch("audiostack.creator.story.Story.interface.send_request")
def test_get_raises_on_500(mock_send: MagicMock) -> None:
    mock_send.side_effect = Exception("Internal server error - aborting")
    with pytest.raises(Exception) as exc_info:
        Story.get("test")
    mock_send.assert_called_once_with(
        rtype="GET", route="story", path_parameters="test"
    )
    assert str(exc_info.value) == "Internal server error - aborting"
