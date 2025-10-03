from typing import Any, Dict, Optional

from audiostack.helpers.api_item import APIResponseItem
from audiostack.helpers.request_interface import RequestInterface
from audiostack.helpers.request_types import RequestTypes


class Brief:
    FAMILY = "creator"
    interface = RequestInterface(family=FAMILY)

    class Item(APIResponseItem):
        def __init__(self, response: dict) -> None:
            super().__init__(response)

            if (
                "data" in response
                and response["data"]
                and "audioforms" in response["data"]
            ):
                self.audioforms = response["data"]["audioforms"]
            else:
                self.audioforms = []

        def is_success(self) -> bool:
            """Check if the creative brief was successfully processed"""
            errors = self.response.get("errors", [])
            return self.status_code == 200 and not errors

        def is_failed(self) -> bool:
            """Check if the creative brief processing failed"""
            errors = self.response.get("errors", [])
            return self.status_code != 200 or bool(errors)

        def get_error_message(self) -> str:
            """Get error message if processing failed"""
            errors = self.response.get("errors", [])
            if errors:
                return "; ".join(errors)
            return ""

        def get_audioform_count(self) -> int:
            """Get the number of audioforms generated"""
            return len(self.audioforms)

    @staticmethod
    def create(
        brief: Optional[Dict[str, Any]] = None,
        file_id: Optional[str] = None,
        num_ads: int = 3,
        audioform_version: str = "1",
    ) -> "Brief.Item":
        """
        Create a new brief request.

        Args:
            brief: The brief configuration object containing:
                - script: Script configuration with productName,
                  productDescription, adLength (default 30),
                  lang (default null),
                  callToAction, targetAudience, toneOfScript,
                  thirdPerson (default true)
                - voices: Voice or VoiceRecommender configuration (array)
                - sounds: Sound configuration
                - production: ProductionSettings
                - delivery: DeliverySettings
            file_id: UUID of an already uploaded brief file
            num_ads: Number of ads to generate (1-5, default 3)
            audioform_version: Version of the audioform to use (default "1")

        Returns:
            Brief.Item: Response containing audioformId and status

        Raises:
            Exception: If neither brief nor file_id is provided,
                or both are provided
        """
        if brief and file_id:
            raise Exception("Either brief or file_id should be provided, not both")
        if not brief and not file_id:
            raise Exception("Either brief or file_id must be provided")

        body: Dict[str, Any] = {"numAds": num_ads}

        if brief:
            body["brief"] = brief
        else:
            body["fileId"] = file_id

        headers = {"version": audioform_version}

        r = Brief.interface.send_request(
            rtype=RequestTypes.POST, route="brief", json=body, headers=headers
        )
        return Brief.Item(r)
