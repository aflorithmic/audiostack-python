import time
from unittest.mock import Mock, patch

import pytest

from audiostack.content.script import Script
from audiostack.speech.tts import TTS


def test_create_speech_with_script_id(script_item: Script.Item) -> None:
    """Test creating a speech item."""
    speech_item = TTS.create(
        scriptId=script_item.scriptId,
        voice="isaac",
    )
    assert isinstance(speech_item, TTS.Item)


def test_create_speech_with_script_item(script_item: Script.Item) -> None:
    """Test creating a speech item."""
    speech_item = TTS.create(
        scriptItem=script_item,
        voice="isaac",
    )
    assert isinstance(speech_item, TTS.Item)


def test_script_id_and_script_item_conflict(script_item: Script.Item) -> None:
    """Test that an exception is raised when both scriptId and scriptItem are provided."""
    try:
        TTS.create(
            scriptId=script_item.scriptId,
            scriptItem=script_item,
            voice="isaac",
        )
    except Exception as e:
        assert str(e) == "scriptId or scriptItem should be supplied not both"
    else:
        assert False, "Expected an exception to be raised"


def test_create_speech_no_script_id_or_item() -> None:
    """Test that an exception is raised when neither scriptId nor scriptItem is provided."""
    try:
        TTS.create(voice="isaac")
    except Exception as e:
        assert str(e) == "scriptId or scriptItem should be supplied"
    else:
        assert False, "Expected an exception to be raised"


@patch("audiostack.speech.tts.TTS.interface.send_request")
def test_create_speech_with_different_timeout(
    mock_send_request: Mock, script_item: Script.Item
) -> None:
    """Test creating a speech item with a different timeout."""
    mock_send_request.return_value = {"statusCode": 202, "data": {"speechId": "123"}}
    start = time.time()
    with pytest.raises(TimeoutError):
        TTS.create(
            scriptId=script_item.scriptId,
            voice="isaac",
            timeoutThreshold=2,
        )
    elapsed = time.time() - start
    assert 2 < elapsed < 2.5  # Allow a small margin for the timeout to trigger


@patch("audiostack.speech.tts.TTS.interface.send_request")
def test_create_speech_with_retries(
    mock_send_request: Mock, script_item: Script.Item
) -> None:
    """Test creating a speech item with retries."""
    mock_send_request.return_value = {"statusCode": 202, "data": {"speechId": "123"}}
    start = time.time()
    with pytest.raises(TimeoutError):
        TTS.create(
            scriptId=script_item.scriptId,
            voice="isaac",
            timeoutThreshold=2,
            timeoutRetries=3,
        )
    elapsed = time.time() - start
    # The total time should be more than 8 seconds due to 4 attempts (initial + 3 retries) and 2 seconds per attempt
    assert 8 < elapsed < 8.5  # Allow a small margin for the retries to complete
