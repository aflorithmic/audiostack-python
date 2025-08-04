import time
from unittest.mock import Mock, patch

import pytest

from audiostack.content.script import Script
from audiostack.production.mix import Mix
from audiostack.speech.tts import TTS


def test_create_production_with_speech_id(speech_item: TTS.Item) -> None:
    """Test creating a speech item."""
    mix_item = Mix.create(
        speechId=speech_item.speechId,
    )
    assert isinstance(mix_item, Mix.Item)


def test_create_production_with_speech_item(speech_item: TTS.Item) -> None:
    """Test creating a production item with speechItem."""
    mix_item = Mix.create(
        speechItem=speech_item,
    )
    assert isinstance(mix_item, Mix.Item)


def test_script_id_and_speech_item_conflict(
    speech_item: TTS.Item, script_item: Script.Item
) -> None:
    """Test that an exception is raised when both scriptId and speechItem are provided."""
    try:
        Mix.create(
            scriptId=script_item.scriptId,
            speechItem=speech_item,
        )
    except Exception as e:
        assert (
            str(e)
            == "only 1 of the following is required; speechId, speechItem, or scriptId"
        )
    else:
        assert False, "Expected an exception to be raised"


def test_create_production_no_script_id_or_item() -> None:
    """Test that an exception is raised when neither scriptId nor speechItem is provided."""
    try:
        Mix.create()
    except Exception as e:
        assert (
            str(e)
            == "only 1 of the following is required; speechId, speechItem, or scriptId"
        )
    else:
        assert False, "Expected an exception to be raised"


@patch("audiostack.production.mix.Mix.interface.send_request")
def test_create_production_with_different_timeout(mock_send_request: Mock) -> None:
    """Test creating a production item with a different timeout."""
    mock_send_request.return_value = {
        "statusCode": 202,
        "data": {"productionId": "123"},
    }
    start = time.time()
    with pytest.raises(TimeoutError):
        Mix.create(
            speechId="some_speech_id",
            timeoutThreshold=2,
        )
    elapsed_time = time.time() - start
    assert (
        2 < elapsed_time < 2.5
    )  # Allow a small margin for the time taken to raise the exception


@patch("audiostack.production.mix.Mix.interface.send_request")
def test_create_production_with_timeout_retries(
    mock_send_request: Mock, speech_item: TTS.Item
) -> None:
    """Test creating a production item with retries on timeout."""
    mock_send_request.return_value = {
        "statusCode": 202,
        "data": {"productionId": "123"},
    }
    start = time.time()
    with pytest.raises(TimeoutError):
        Mix.create(
            speechId=speech_item.speechId,
            timeoutRetries=3,
            timeoutThreshold=2,
        )
    elapsed_time = time.time() - start
    # The total time should be more than 8 seconds due to 4 attempts (initial + 3 retries) and 2 seconds per attempt
    assert (
        8 < elapsed_time < 8.5
    )  # Allow a small margin for the time taken to raise the exception
