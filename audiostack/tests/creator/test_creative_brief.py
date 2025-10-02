import pytest
from unittest.mock import patch

from audiostack.creator.creative_brief import Brief


class TestCreativeBrief:
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
            "data": [
                {
                    "statusCode": 200,
                    "audioformId": "test-uuid-123",
                    "audioform": {"version": "0.0.1"},
                }
            ],
            "meta": {"creditsUsed": 1.0},
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
            )

            assert result.status_code == 200
            assert result.audioform_id == "test-uuid-123"
            assert result.audioform == {"version": "0.0.1"}

    def test_create_with_field_id(self) -> None:
        """Test creating creative brief with field_id"""
        field_id = "uploaded-brief-uuid-456"

        mock_response = {
            "data": [
                {
                    "statusCode": 200,
                    "audioformId": "test-uuid-789",
                    "audioform": {"version": "1"},
                }
            ],
            "meta": {"creditsUsed": 1.5},
        }

        with patch.object(
            Brief.interface, "send_request", return_value=mock_response
        ) as mock_send:
            result = Brief.create(field_id=field_id, num_ads=5)

            mock_send.assert_called_once_with(
                rtype="POST",
                route="brief",
                json={
                    "fieldId": field_id,
                    "numAds": 5,
                },
            )

            assert result.status_code == 200
            assert result.audioform_id == "test-uuid-789"

    def test_create_with_defaults(self) -> None:
        """Test creating creative brief with default parameters"""
        brief_config = {
            "script": {"productName": "Test Product"},
            "voices": [{"speed": None}],
        }

        mock_response = {
            "data": [
                {
                    "statusCode": 200,
                    "audioformId": "test-uuid-default",
                    "audioform": {},
                }
            ]
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
            )

    def test_create_error_both_provided(self) -> None:
        """Test error when both brief and field_id are provided"""
        brief_config = {"script": {"productName": "Test"}}
        field_id = "test-uuid"

        with pytest.raises(Exception) as exc_info:
            Brief.create(brief=brief_config, field_id=field_id)

        assert ("Either brief or field_id should be provided, not both" in
                str(exc_info.value))

    def test_create_error_none_provided(self) -> None:
        """Test error when neither brief nor field_id is provided"""
        with pytest.raises(Exception) as exc_info:
            Brief.create()

        assert ("Either brief or field_id must be provided" in
                str(exc_info.value))

    def test_item_class_properties(self) -> None:
        """Test CreativeBrief.Item class properties"""
        response_data = {
            "data": [
                {
                    "statusCode": 201,
                    "audioformId": "item-test-uuid",
                    "audioform": {"version": "0.0.1", "status": "processing"},
                }
            ],
            "meta": {"creditsUsed": 2.0},
        }

        item = Brief.Item(response_data)

        assert item.status_code == 201
        assert item.audioform_id == "item-test-uuid"
        assert item.audioform == {"version": "0.0.1", "status": "processing"}
        assert item.meta == {"creditsUsed": 2.0}

    def test_item_class_empty_data(self) -> None:
        """Test CreativeBrief.Item with empty data"""
        response_data: dict = {"data": []}

        item = Brief.Item(response_data)

        assert item.status_code == 200
        assert item.audioform_id == ""
        assert item.audioform == {}
