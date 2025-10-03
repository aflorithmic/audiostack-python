from unittest.mock import patch

import pytest

from audiostack.creator.brief import Brief


class TestBrief:
    def test_create_with_brief_config(self) -> None:
        """Test creating creative brief with brief configuration"""
        brief_config = {
            "script": {
                "productName": "Test Product",
                "productDescription": "A great product",
                "adLength": 30,
                "thirdPerson": True,
            },
            "voices": [{"speed": None}],
            "sounds": {"soundDesign": [{"alias": None, "useSmartFit": True}]},
            "production": {"masteringPreset": "balanced"},
            "delivery": {
                "encoderPreset": "mp3",
                "loudnessPreset": "spotify",
                "public": True,
            },
        }

        mock_response = {
            "statusCode": 200,
            "message": "Creative brief processed into audioforms",
            "warnings": [],
            "data": {
                "audioforms": [
                    {
                        "statusCode": 202,
                        "audioformId": "test-uuid-123",
                        "audioform": {
                            "audioform": {
                                "header": {"version": "0.0.1"},
                                "assets": {},
                                "production": {},
                                "delivery": {},
                            }
                        },
                    }
                ]
            },
            "meta": {
                "version": "123",
                "requestId": "test-request-id",
                "creditsUsed": 1.0,
                "creditsRemaining": 245.5,
            },
        }

        with patch.object(
            Brief.interface, "send_request", return_value=mock_response
        ) as mock_send:
            result = Brief.create(brief=brief_config, num_ads=3)

            mock_send.assert_called_once_with(
                rtype="POST",
                route="brief",
                json={
                    "brief": brief_config,
                    "numAds": 3,
                },
                headers={"version": "1"},
            )

            assert result.status_code == 200
            assert len(result.audioforms) == 1
            assert result.get_audioform_count() == 1
            assert result.is_success()

            first_audioform = result.audioforms[0]
            assert first_audioform["audioformId"] == "test-uuid-123"
            assert (
                first_audioform["audioform"]["audioform"]["header"]["version"]
                == "0.0.1"
            )

    def test_create_with_file_id(self) -> None:
        """Test creating creative brief with file_id"""
        file_id = "uploaded-brief-uuid-456"

        mock_response = {
            "statusCode": 200,
            "message": "Creative brief processed into audioforms",
            "warnings": [],
            "data": {
                "audioforms": [
                    {
                        "statusCode": 202,
                        "audioformId": "test-uuid-789",
                        "audioform": {
                            "audioform": {
                                "header": {"version": "1"},
                                "assets": {},
                                "production": {},
                                "delivery": {},
                            }
                        },
                    }
                ]
            },
            "meta": {
                "version": "123",
                "requestId": "test-request-id-2",
                "creditsUsed": 1.5,
                "creditsRemaining": 244.0,
            },
        }

        with patch.object(
            Brief.interface, "send_request", return_value=mock_response
        ) as mock_send:
            result = Brief.create(file_id=file_id, num_ads=5)

            mock_send.assert_called_once_with(
                rtype="POST",
                route="brief",
                json={
                    "fileId": file_id,
                    "numAds": 5,
                },
                headers={"version": "1"},
            )

            assert result.status_code == 200
            assert len(result.audioforms) == 1
            assert result.get_audioform_count() == 1

            first_audioform = result.audioforms[0]
            assert first_audioform["audioformId"] == "test-uuid-789"

    def test_create_with_defaults(self) -> None:
        """Test creating creative brief with default parameters"""
        brief_config = {
            "script": {"productName": "Test Product"},
            "voices": [{"speed": None}],
        }

        mock_response = {
            "statusCode": 200,
            "message": "Creative brief processed into audioforms",
            "warnings": [],
            "data": {
                "audioforms": [
                    {
                        "statusCode": 202,
                        "audioformId": "test-uuid-default",
                        "audioform": {
                            "audioform": {
                                "header": {"version": "0.0.1"},
                                "assets": {},
                                "production": {},
                                "delivery": {},
                            }
                        },
                    }
                ]
            },
            "meta": {
                "version": "123",
                "requestId": "test-request-id-3",
                "creditsUsed": 0,
                "creditsRemaining": 245.5,
            },
        }

        with patch.object(
            Brief.interface, "send_request", return_value=mock_response
        ) as mock_send:
            Brief.create(brief=brief_config)

            mock_send.assert_called_once_with(
                rtype="POST",
                route="brief",
                json={
                    "brief": brief_config,
                    "numAds": 3,  # default value
                },
                headers={"version": "1"},  # default value
            )

    def test_create_error_both_provided(self) -> None:
        """Test error when both brief and file_id are provided"""
        brief_config = {"script": {"productName": "Test"}}
        file_id = "test-uuid"

        with pytest.raises(Exception) as exc_info:
            Brief.create(brief=brief_config, file_id=file_id)

        assert "Either brief or file_id should be provided, not both" in str(
            exc_info.value
        )

    def test_create_error_none_provided(self) -> None:
        """Test error when neither brief nor file_id is provided"""
        with pytest.raises(Exception) as exc_info:
            Brief.create()

        assert "Either brief or file_id must be provided" in str(exc_info.value)

    def test_item_class_properties(self) -> None:
        """Test CreativeBrief.Item class properties"""
        response_data = {
            "statusCode": 201,
            "message": "Creative brief processed into audioforms",
            "warnings": [],
            "data": {
                "audioforms": [
                    {
                        "statusCode": 202,
                        "audioformId": "item-test-uuid",
                        "audioform": {
                            "audioform": {"version": "0.0.1", "status": "processing"}
                        },
                    }
                ]
            },
            "meta": {
                "version": "123",
                "requestId": "test-request-id-4",
                "creditsUsed": 2.0,
                "creditsRemaining": 243.5,
            },
        }

        item = Brief.Item(response_data)

        assert item.status_code == 201
        assert item.meta == {
            "version": "123",
            "requestId": "test-request-id-4",
            "creditsUsed": 2.0,
            "creditsRemaining": 243.5,
        }
        assert len(item.audioforms) == 1
        assert item.get_audioform_count() == 1

        first_audioform = item.audioforms[0]
        assert first_audioform["audioformId"] == "item-test-uuid"
        assert first_audioform["audioform"]["audioform"]["version"] == "0.0.1"

    def test_item_class_empty_data(self) -> None:
        """Test CreativeBrief.Item with empty data"""
        response_data: dict = {
            "statusCode": 200,
            "message": "Creative brief processed into audioforms",
            "warnings": [],
            "data": {"audioforms": []},
            "meta": {
                "version": "123",
                "requestId": "test-request-id-5",
                "creditsUsed": 0,
                "creditsRemaining": 245.5,
            },
        }

        item = Brief.Item(response_data)

        assert item.status_code == 200
        assert len(item.audioforms) == 0
        assert item.get_audioform_count() == 0

    def test_item_class_error_response(self) -> None:
        """Test CreativeBrief.Item with error response (422)"""
        response_data = {
            "statusCode": 422,
            "message": "Failed to process brief.",
            "warnings": [],
            "errors": [
                (
                    "Invalid value for field `brief.script.ScriptWriter`: "
                    "Value error, Either 'productDescription' or 'scriptText' "
                    "must be provided, but not both."
                ),
                (
                    "Invalid value for field `brief.script.PrewrittenScript`: "
                    "Value error, Either 'productDescription' or 'scriptText' "
                    "must be provided, but not both."
                ),
            ],
            "data": {"audioforms": []},
            "meta": {
                "version": "123",
                "requestId": "test-request-id-6",
                "creditsUsed": 0,
                "creditsRemaining": 245.5,
            },
        }

        item = Brief.Item(response_data)

        assert item.status_code == 422
        assert len(item.audioforms) == 0
        assert item.get_audioform_count() == 0
        assert item.is_failed()
        assert not item.is_success()
        assert (
            "Either 'productDescription' or 'scriptText' must be provided"
            in item.get_error_message()
        )
