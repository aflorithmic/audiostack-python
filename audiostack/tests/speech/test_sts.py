from typing import Any
from unittest.mock import Mock, call, patch

import pytest
from pytest import fixture

from audiostack.speech.sts import STS


@fixture
def voice_data() -> dict:
    return {
        "provider": "provider",
        "alias": "alias",
        "language": "language",
        "languageCode": "languageCode",
    }


@fixture
def pipelineFinishedItem_data() -> dict:
    return {
        "pipelineId": "pipelineId",
        "results": {
            "newFileIds": "newFileIds",
            "inputFileIds": "inputFileIds",
            "replacedFileIds": "replacedFileIds",
        },
    }


@fixture
def mock_send_request() -> Any:
    with patch("audiostack.speech.STS.interface.send_request") as mock_:
        yield mock_


@fixture
def mock__poll() -> Any:
    with patch("audiostack.speech.STS._poll") as mock_:
        yield mock_


def test_Sts_family() -> None:
    assert STS.interface.family == "speech/sts"


def test_StsVoiceItem(voice_data: dict) -> None:
    response = {"data": voice_data}
    item = STS.StsVoiceItem(response=response)
    assert item.provider == voice_data["provider"]
    assert item.alias == voice_data["alias"]
    assert item.language == voice_data["language"]
    assert item.languageCode == voice_data["languageCode"]
    assert item.response == response


def test_PipelineInProgressItem() -> None:
    response = {"data": {"pipelineId": "pipelineId"}}
    item = STS.PipelineInProgressItem(response=response)
    assert item.pipelineId == "pipelineId"
    assert item.response == response


def test_PipelineFinishedItem(pipelineFinishedItem_data: dict) -> None:
    response = {"data": pipelineFinishedItem_data}
    item = STS.PipelineFinishedItem(response=response)
    assert item.pipelineId == "pipelineId"
    assert item.inputFileIds == "inputFileIds"
    assert item.replacedFileIds == "replacedFileIds"
    assert item.response == response


def test_STS_voices(mock_send_request: Mock, voice_data: dict) -> None:
    mock_send_request.return_value = {"data": {"voices": [voice_data] * 10}}

    r = STS.voices()
    mock_send_request.assert_called_once_with(rtype="GET", route="voices")
    item = r[0]
    # assert item.provider == "provider" # fails
    assert item["provider"] == voice_data["provider"]
    assert item["alias"] == voice_data["alias"]
    assert item["language"] == voice_data["language"]
    assert item["languageCode"] == voice_data["languageCode"]


def test_STS_create(mock_send_request: Mock) -> None:
    alias = "alias"
    fileId = "fileId"
    mock_send_request.return_value = {"data": {"pipelineId": "pipelineId"}}
    r = STS.create(alias=alias, fileId=fileId)
    mock_send_request.assert_called_once_with(
        rtype="POST", route="", json={"alias": "alias", "fileId": "fileId"}
    )
    assert isinstance(r, STS.PipelineInProgressItem)
    assert r.pipelineId == "pipelineId"


def test_STS_create_newFilePath(mock_send_request: Mock) -> None:
    alias = "alias"
    fileId = "fileId"
    newFilePath = "newFilePath"
    mock_send_request.return_value = {"data": {"pipelineId": "pipelineId"}}
    r = STS.create(alias=alias, fileId=fileId, newFilePath=newFilePath)
    mock_send_request.assert_called_once_with(
        rtype="POST",
        route="",
        json={"alias": "alias", "fileId": "fileId", "newFilePath": "newFilePath"},
    )
    assert isinstance(r, STS.PipelineInProgressItem)
    assert r.pipelineId == "pipelineId"


@pytest.mark.parametrize("status_code", [200, 202])
def test_STS_get(
    mock_send_request: Mock,
    mock__poll: Mock,
    pipelineFinishedItem_data: dict,
    status_code: int,
) -> None:
    pipelineId = "pipelineId"
    mock_data = {**{"status": status_code}, **pipelineFinishedItem_data}
    mock_send_request.return_value = {"data": mock_data}
    mock__poll.return_value = STS.PipelineFinishedItem({"data": mock_data})
    r = STS.get(pipelineId=pipelineId)
    mock_send_request.assert_called_once_with(
        rtype="GET", route="", path_parameters=pipelineId
    )
    assert r == mock__poll.return_value


def test_STS_get_raises_FailedStatusFetch(mock_send_request: Mock) -> None:
    pipelineId = "pipelineId"
    mock_send_request.return_value = {"data": {"status": 404, "body": "error message"}}

    with pytest.raises(STS.FailedStatusFetch) as exc:
        STS.get(pipelineId=pipelineId)

    assert str(exc.value) == "Failed to fetch pipeline with error: error message"


def test_STS__poll(mock_send_request: Mock, pipelineFinishedItem_data: dict) -> None:
    r = {"data": {"status": 202}}

    # with statusCode 202 the request is executed again until it gets 200
    return_value_1 = {"data": {**{"status": 202}, **pipelineFinishedItem_data}}
    return_value_2 = {"data": {**{"status": 200}, **pipelineFinishedItem_data}}
    mock_send_request.side_effect = [return_value_1, return_value_2]

    response = STS._poll(r=r, pipelineId="pipelineId")
    mock_send_request.assert_has_calls(
        [
            call(rtype="GET", route="", path_parameters="pipelineId"),
            call(rtype="GET", route="", path_parameters="pipelineId"),
        ]
    )
    assert isinstance(response, STS.PipelineFinishedItem)
    assert response.data == return_value_2["data"]


def test_STS__poll_400(
    mock_send_request: Mock, pipelineFinishedItem_data: dict
) -> None:
    r = {"data": {**{"status": 202}, **pipelineFinishedItem_data}}

    mock_send_request.return_value = {
        "data": {
            "status": 404,
            "message": "message",
            "errors": "errors",
        }
    }

    with pytest.raises(STS.FailedPipeline):
        STS._poll(r=r, pipelineId="pipelineId")
