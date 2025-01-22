import os
from typing import Any
from unittest.mock import Mock, patch

from pytest import fixture

import audiostack
from audiostack.helpers.api_item import APIResponseItem
from audiostack.helpers.request_types import RequestTypes
from audiostack.speech.voice import Voice

audiostack.api_base = os.environ.get("AUDIO_STACK_DEV_URL", "https://v2.api.audio")
audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]  # type: ignore


@fixture
def voice_data() -> dict:
    return {
        "response": "response",
        "provider": "provider",
        "alias": "alias",
    }


@fixture
def mock_send_request() -> Any:
    with patch("audiostack.speech.Voice.interface.send_request") as mock_:
        yield mock_


def test_item(voice_data: dict) -> None:
    v = Voice.Item({"data": voice_data})
    assert v.provider
    assert v.alias
    assert v.response


def test_list() -> None:
    voices = Voice.list()
    for v in voices:
        assert isinstance(v, Voice.Item)
        assert v.provider
        assert v.alias
        assert v.data


def test_parmaters() -> None:
    r = Voice.Parameter.get()
    assert r


def test_Voice_query(mock_send_request: Mock, voice_data: dict) -> None:
    mock_send_request.return_value = {"data": {"voices": [voice_data] * 10}}
    voices = Voice.query()
    mock_send_request.assert_called_once_with(
        rtype=RequestTypes.POST,
        route="query",
        json={
            "filters": [],
            "minimumNumberOfResults": 3,
            "forceApplyFilters": True,
            "page": 1,
            "pageLimit": 1000,
        },
    )
    assert isinstance(voices, Voice.List)
    assert voices.data == {"voices": [voice_data] * 10}


def test_Voice_query_with_parameters(mock_send_request: Mock, voice_data: dict) -> None:
    mock_send_request.return_value = {"data": {"voices": [voice_data] * 10}}
    filters = [{"in": {"language": ["dutch"]}}]
    voices = Voice.query(
        filters=filters,
        minimumNumberOfResults=1,
        forceApplyFilters=False,
        pageLimit=100,
    )
    mock_send_request.assert_called_once_with(
        rtype=RequestTypes.POST,
        route="query",
        json={
            "filters": filters,
            "minimumNumberOfResults": 1,
            "forceApplyFilters": False,
            "page": 1,
            "pageLimit": 100,
        },
    )
    assert isinstance(voices, Voice.List)
    assert voices.data == {"voices": [voice_data] * 10}


def test_Voice_select_for_script(mock_send_request: Mock, voice_data: dict) -> None:
    mock_send_request.return_value = voice_data
    r = Voice.select_for_script(scriptId="1")
    mock_send_request.assert_called_once_with(
        rtype=RequestTypes.POST,
        route="select",
        json={"scriptId": "1", "tone": "", "targetLength": 20},
    )
    assert isinstance(r, APIResponseItem)
    assert r.response == voice_data
