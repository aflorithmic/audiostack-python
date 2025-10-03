from unittest.mock import Mock, patch

from audiostack.audioform.audioform import Audioform
from audiostack.helpers.request_types import RequestTypes

# ============================================================================
# POST ENDPOINT TESTS (Audioform.create)
# ============================================================================


@patch("audiostack.audioform.audioform.Audioform.interface.send_request")
def test_audioform_create_v1(mock_send_request: Mock) -> None:
    """Test Audioform.create method with v1 payload"""
    mock_response = {
        "metadata": {
            "requestId": "request_id_test",
            "version": "1",
            "creditUsed": 0.0,
            "creditsRemaining": 0.0,
        },
        "warnings": [],
        "message": "Audioform successfully posted",
        "data": {"audioformId": "new-audioform-v1-123"},
    }
    mock_send_request.return_value = mock_response

    audioform_config = {
        "assets": {
            "script 0": {"type": "tts", "voiceRef": "voice 0", "text": "Some text"},
            "sound template": {
                "type": "soundTemplate",
                "soundTemplateAlias": "an alias",
                "segment": "main",
            },
            "sound template snippet": {
                "type": "soundTemplateSnippet",
                "soundTemplateRef": "sound template",
                "targetDuration": 5.0,
                "targetReadPosition": 0.0,
            },
            "media 0": {"type": "media", "mediaId": "some uuid"},
            "voice 0": {"type": "voice", "voiceAlias": "Alex", "speed": 1},
            "the sts media": {"type": "media", "mediaId": "some uuid"},
            "the sts voice": {"type": "voice", "voiceAlias": "isaac"},
            "script 1": {
                "type": "sts",
                "mediaRef": "the sts media",
                "voiceRef": "the sts voice",
            },
            "sound effect 0": {"type": "soundEffect", "soundEffectAlias": "animals_0"},
        },
        "production": {
            "arrangement": {
                "sections": [
                    {
                        "layers": [
                            {
                                "clips": [
                                    {"assetRef": "script 0"},
                                    {"assetRef": "media 0"},
                                    {
                                        "assetRef": "sound effect 0",
                                        "readPosition": 2,
                                        "forcedDuration": 3,
                                        "fadeIn": 0.5,
                                        "fadeOut": 0.5,
                                        "marginStart": 0.5,
                                        "marginEnd": 0.5,
                                    },
                                ],
                                "alignment": "middle",
                            }
                        ]
                    }
                ]
            },
            "masteringPreset": "preset 0",
        },
        "delivery": {"loudnessPreset": "radio", "encoderPreset": "mp3"},
    }

    result = Audioform.create(audioform_config)

    assert isinstance(result, Audioform.Item)
    assert result.audioform_id == "new-audioform-v1-123"
    assert result.status_code == 200

    mock_send_request.assert_called_once_with(
        rtype=RequestTypes.POST, route="", json={"audioform": audioform_config}
    )


@patch("audiostack.audioform.audioform.Audioform.interface.send_request")
def test_audioform_create_v001(mock_send_request: Mock) -> None:
    """Test Audioform.create method with v0.0.1 payload"""
    mock_response = {
        "metadata": {
            "requestId": "request_id_test",
            "version": "0.0.1",
            "creditUsed": 0.0,
            "creditsRemaining": 0.0,
        },
        "warnings": [],
        "message": "Audioform successfully posted",
        "data": {"audioformId": "new-audioform-v001-123"},
    }
    mock_send_request.return_value = mock_response

    audioform_config = {
        "assets": {
            "media 0": {
                "type": "media",
                "mediaId": "7f3ea7ec-63d3-44d4-8ef5-5937eaaf0ee4",
            },
            "script 0": {
                "type": "tts",
                "text": (
                    "This is a section of a script used to test the "
                    "audioform version three service."
                ),
                "voiceRef": "main voice",
                "targetDuration": 4.1,
            },
            "the sts media": {
                "type": "media",
                "mediaId": "600b445f-dbec-4d7b-9912-acef10ba94bb",
            },
            "script 1": {
                "type": "sts",
                "mediaRef": "the sts media",
                "voiceRef": "the sts voice",
                "targetDuration": 10.1,
            },
            "main voice": {"type": "voice", "voiceId": "Sara", "speed": 0.98},
            "the sts voice": {"type": "voice", "voiceId": "isaac"},
            "sound template 0": {
                "type": "soundTemplate",
                "soundTemplateId": "soiree_a_illange",
                "segment": "main",
            },
            "sound template snippet": {
                "type": "soundTemplateSnippet",
                "soundTemplateRef": "sound template 0",
                "targetDuration": 5.0,
            },
            "sound effect": {
                "type": "soundEffect",
                "soundEffectId": "a sound template alias",
            },
        },
        "production": {
            "arrangement": {
                "forcedDuration": 20,
                "sections": [
                    {
                        "layers": [
                            {
                                "clips": [
                                    {
                                        "assetId": "script 0",
                                        "fadeIn": 0.5,
                                        "forcedDuration": 4.1,
                                    },
                                    {
                                        "assetId": "media 0",
                                        "fadeOut": 0.5,
                                        "marginStart": 0.5,
                                        "marginEnd": 0.5,
                                    },
                                    {"assetId": "script 1"},
                                ]
                            },
                            {
                                "clips": [
                                    {
                                        "assetId": "media 0",
                                        "readPosition": 5,
                                        "forcedDuration": 0.5,
                                    },
                                    {"assetId": "sound template snippet"},
                                ],
                                "alignment": "end",
                            },
                        ],
                        "soundTemplateId": "sound template 0",
                        "paddingStart": 0.5,
                        "paddingEnd": 1.5,
                    },
                    {
                        "layers": [{"clips": [{"assetId": "media 0"}]}],
                        "fadeIn": 0.5,
                        "fadeOut": 1.5,
                    },
                ],
            },
            "masteringPreset": "balanced",
        },
        "delivery": {
            "loudnessPreset": "radio",
            "encoderPreset": "mp3",
            "public": False,
        },
    }

    result = Audioform.create(audioform_config)

    assert isinstance(result, Audioform.Item)
    assert result.audioform_id == "new-audioform-v001-123"
    assert result.status_code == 200

    mock_send_request.assert_called_once_with(
        rtype=RequestTypes.POST, route="", json={"audioform": audioform_config}
    )


@patch("audiostack.audioform.audioform.Audioform.interface.send_request")
def test_audioform_create_validation_error(mock_send_request: Mock) -> None:
    """Test Audioform.create method with validation error (422)"""
    mock_response = {
        "statusCode": 422,
        "message": "Validation failed",
        "errors": [
            "assets is required",
            "production is required",
            "delivery is required",
        ],
    }
    mock_send_request.return_value = mock_response

    audioform_config = {"header": {"version": "1"}}

    result = Audioform.create(audioform_config)

    assert isinstance(result, Audioform.Item)
    assert result.audioform_id == ""
    assert result.status_code == 422
    assert result.errors == [
        "assets is required",
        "production is required",
        "delivery is required",
    ]

    mock_send_request.assert_called_once_with(
        rtype=RequestTypes.POST, route="", json={"audioform": audioform_config}
    )


@patch("audiostack.audioform.audioform.Audioform.interface.send_request")
def test_audioform_create_invalid_version(mock_send_request: Mock) -> None:
    """Test Audioform.create method with invalid version"""
    mock_response = {
        "statusCode": 400,
        "message": "Invalid version",
        "errors": ["version must be '1' or '0.0.1'"],
    }
    mock_send_request.return_value = mock_response

    audioform_config = {
        "assets": {"test": {"type": "tts", "text": "test"}},
        "production": {"masteringPreset": "balanced"},
        "delivery": {"encoderPreset": "mp3"},
    }

    result = Audioform.create(audioform_config)

    assert isinstance(result, Audioform.Item)
    assert result.audioform_id == ""
    assert result.status_code == 400
    assert result.errors == ["version must be '1' or '0.0.1'"]

    mock_send_request.assert_called_once_with(
        rtype=RequestTypes.POST, route="", json={"audioform": audioform_config}
    )


@patch("audiostack.audioform.audioform.Audioform.interface.send_request")
def test_audioform_create_immediate_return(mock_send_request: Mock) -> None:
    """Test Audioform.create method returns immediately"""
    mock_response = {
        "metadata": {
            "requestId": "request_id_test",
            "version": "1",
            "creditUsed": 0.0,
            "creditsRemaining": 0.0,
        },
        "warnings": [],
        "message": "Audioform successfully posted",
        "data": {"audioformId": "immediate-audioform-123"},
    }
    mock_send_request.return_value = mock_response

    audioform_config = {
        "header": {"version": "1"},
        "assets": {"script 0": {"type": "tts", "text": "test"}},
        "production": {"masteringPreset": "balanced"},
        "delivery": {"encoderPreset": "mp3"},
    }

    result = Audioform.create(audioform_config)

    assert isinstance(result, Audioform.Item)
    assert result.audioform_id == "immediate-audioform-123"
    assert result.status_code == 200

    mock_send_request.assert_called_once_with(
        rtype=RequestTypes.POST, route="", json={"audioform": audioform_config}
    )


# ============================================================================
# GET ENDPOINT TESTS (Audioform.get)
# ============================================================================


@patch("audiostack.audioform.audioform.Audioform.interface.send_request")
def test_audioform_get_v1(mock_send_request: Mock) -> None:
    """Test Audioform.get method with v1 version"""
    mock_response = {
        "data": {
            "audioformId": "existing-audioform-v1-123",
            "statusCode": 200,
            "audioform": {
                "header": {"version": "1"},
                "assets": {"script 0": {"type": "tts", "text": "test"}},
                "production": {"masteringPreset": "balanced"},
                "delivery": {"encoderPreset": "mp3"},
            },
            "result": {
                "header": {"version": "1", "audioformId": "existing-audioform-v1-123"},
                "assets": {"script 0": {"type": "tts", "duration": 4.95}},
                "production": {"masteringPreset": "balanced"},
                "delivery": {"encoderPreset": "mp3"},
            },
        },
        "statusCode": 200,
        "message": "Audioform retrieved",
    }
    mock_send_request.return_value = mock_response

    result = Audioform.get("existing-audioform-v1-123", version="1")

    assert isinstance(result, Audioform.Item)
    assert result.audioform_id == "existing-audioform-v1-123"
    assert result.status_code == 200
    assert result.audioform["header"]["version"] == "1"
    assert result.result["header"]["version"] == "1"

    mock_send_request.assert_called_once_with(
        rtype=RequestTypes.GET,
        route="",
        path_parameters="existing-audioform-v1-123",
        headers={"version": "1"},
    )


@patch("audiostack.audioform.audioform.Audioform.interface.send_request")
def test_audioform_get_v001(mock_send_request: Mock) -> None:
    """Test Audioform.get method with v0.0.1 version"""
    mock_response = {
        "data": {
            "audioformId": "existing-audioform-v001-123",
            "statusCode": 200,
            "audioform": {
                "header": {"version": "0.0.1"},
                "assets": {"script 0": {"type": "tts", "text": "test"}},
                "production": {"masteringPreset": "balanced"},
                "delivery": {"encoderPreset": "mp3"},
            },
            "result": {
                "header": {
                    "version": "0.0.1",
                    "audioformId": "existing-audioform-v001-123",
                },
                "assets": {"script 0": {"type": "tts", "durationInSecond": 4.95}},
                "production": {"masteringPreset": "balanced"},
                "delivery": {"encoderPreset": "mp3"},
            },
        },
        "statusCode": 200,
        "message": "Audioform retrieved",
    }
    mock_send_request.return_value = mock_response

    result = Audioform.get("existing-audioform-v001-123", version="0.0.1")

    assert isinstance(result, Audioform.Item)
    assert result.audioform_id == "existing-audioform-v001-123"
    assert result.status_code == 200
    assert result.audioform["header"]["version"] == "0.0.1"
    assert result.result["header"]["version"] == "0.0.1"

    mock_send_request.assert_called_once_with(
        rtype=RequestTypes.GET,
        route="",
        path_parameters="existing-audioform-v001-123",
        headers={"version": "0.0.1"},
    )


@patch("audiostack.audioform.audioform.Audioform.interface.send_request")
def test_audioform_get_not_found(mock_send_request: Mock) -> None:
    """Test Audioform.get method with not found response"""
    mock_response = {"statusCode": 404, "message": "Audioform not found"}
    mock_send_request.return_value = mock_response

    result = Audioform.get("nonexistent-audioform-123")

    assert isinstance(result, Audioform.Item)
    assert result.audioform_id == ""
    assert result.status_code == 404


@patch("audiostack.audioform.audioform.Audioform.interface.send_request")
def test_audioform_get_success(mock_send_request: Mock) -> None:
    """Test Audioform.get method with successful result"""
    mock_response = {
        "data": {
            "audioformId": "success-audioform-123",
            "statusCode": 200,
            "audioform": {
                "header": {"version": "1"},
                "assets": {"script 0": {"type": "tts", "text": "test"}},
                "production": {"masteringPreset": "balanced"},
                "delivery": {"encoderPreset": "mp3"},
            },
            "result": {
                "header": {"version": "1", "audioformId": "success-audioform-123"},
                "assets": {"script 0": {"type": "tts", "duration": 4.95}},
                "production": {"masteringPreset": "balanced"},
                "delivery": {"encoderPreset": "mp3"},
            },
        },
        "statusCode": 200,
        "message": "Audioform completed successfully",
    }
    mock_send_request.return_value = mock_response

    result = Audioform.get("success-audioform-123", version="1")

    assert isinstance(result, Audioform.Item)
    assert result.audioform_id == "success-audioform-123"
    assert result.status_code == 200
    assert result.is_success()
    assert not result.is_failed()
    assert not result.is_in_progress()
    assert result.get_error_message() == ""

    mock_send_request.assert_called_once_with(
        rtype=RequestTypes.GET,
        route="",
        path_parameters="success-audioform-123",
        headers={"version": "1"},
    )


@patch("audiostack.audioform.audioform.Audioform.interface.send_request")
def test_audioform_get_failed(mock_send_request: Mock) -> None:
    """Test Audioform.get method with failed result"""
    mock_response = {
        "data": {
            "audioformId": "failed-audioform-123",
            "statusCode": 200,
            "audioform": {
                "header": {"version": "1"},
                "assets": {
                    "script 0": {
                        "type": "tts",
                        "text": "test",
                        "voiceRef": "nonexistent",
                    }
                },
                "production": {"masteringPreset": "balanced"},
                "delivery": {"encoderPreset": "mp3"},
            },
            "result": {},
            "errors": ["Voice 'nonexistent' not found"],
        },
        "statusCode": 200,
        "message": "Audioform processing failed",
    }
    mock_send_request.return_value = mock_response

    result = Audioform.get("failed-audioform-123", version="1")

    assert isinstance(result, Audioform.Item)
    assert result.audioform_id == "failed-audioform-123"
    assert result.status_code == 200
    assert not result.is_success()
    assert result.is_failed()
    assert not result.is_in_progress()
    assert result.get_error_message() == "Voice 'nonexistent' not found"

    mock_send_request.assert_called_once_with(
        rtype=RequestTypes.GET,
        route="",
        path_parameters="failed-audioform-123",
        headers={"version": "1"},
    )


@patch("audiostack.audioform.audioform.Audioform.interface.send_request")
def test_audioform_get_with_polling(mock_send_request: Mock) -> None:
    """Test Audioform.get method with polling behavior"""
    mock_response_in_progress = {
        "message": "Audioform is still being processed",
        "audioformId": "polling-audioform-123",
    }

    mock_response_completed = {
        "data": {
            "audioformId": "polling-audioform-123",
            "statusCode": 200,
            "audioform": {
                "header": {"version": "1"},
                "assets": {"script 0": {"type": "tts", "text": "test"}},
                "production": {"masteringPreset": "balanced"},
                "delivery": {"encoderPreset": "mp3"},
            },
            "result": {
                "header": {"version": "1", "audioformId": "polling-audioform-123"},
                "assets": {"script 0": {"type": "tts", "duration": 4.95}},
                "production": {"masteringPreset": "balanced"},
                "delivery": {"encoderPreset": "mp3"},
            },
        },
        "statusCode": 200,
        "message": "Audioform completed",
    }

    mock_send_request.side_effect = [mock_response_in_progress, mock_response_completed]

    result = Audioform.get("polling-audioform-123", version="1")

    assert isinstance(result, Audioform.Item)
    assert result.audioform_id == "polling-audioform-123"
    assert result.status_code == 200
    assert result.is_success()
    assert not result.is_failed()
    assert not result.is_in_progress()

    # Should have made 2 calls: GET (in progress), GET (completed)
    assert mock_send_request.call_count == 2


# ============================================================================
# ITEM CLASS TESTS (Audioform.Item)
# ============================================================================


@patch("audiostack.audioform.audioform.Audioform.get")
def test_audioform_item_get(mock_get: Mock) -> None:
    """Test Audioform.Item.get method"""
    mock_response = Audioform.Item(
        {"data": {"audioformId": "test-id", "statusCode": 200}}
    )
    mock_get.return_value = mock_response

    item = Audioform.Item({"data": {"audioformId": "test-id"}})

    result = item.get()

    assert result == mock_response
    mock_get.assert_called_once_with("test-id")


def test_audioform_item_initialisation_malformed_data() -> None:
    """Test Audioform.Item initialisation with malformed response data"""
    response_data = {"statusCode": 200, "message": "Success"}

    item = Audioform.Item(response_data)

    assert item.audioform_id == ""
    assert item.status_code == 200
    assert item.audioform == {}
    assert item.result == {}


def test_audioform_item_initialisation_partial_data() -> None:
    """Test Audioform.Item initialisation with partial data"""
    response_data = {
        "data": {
            "audioformId": "partial-test-123",
            # Missing statusCode, audioform, result
        },
        "statusCode": 200,
        "message": "Success",
    }

    item = Audioform.Item(response_data)

    assert item.audioform_id == "partial-test-123"
    assert item.status_code == 200
    assert item.audioform == {}
    assert item.result == {}


def test_audioform_item_initialisation_none_data() -> None:
    """Test Audioform.Item initialisation with None data"""
    response_data = {"data": None, "statusCode": 200, "message": "Success"}

    item = Audioform.Item(response_data)

    assert item.audioform_id == ""
    assert item.status_code == 200
    assert item.audioform == {}
    assert item.result == {}
