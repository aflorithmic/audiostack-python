from typing import Any, Dict, Optional

from audiostack.helpers.api_item import APIResponseItem
from audiostack.helpers.request_interface import RequestInterface
from audiostack.helpers.request_types import RequestTypes


class CreativeBrief:
    FAMILY = "creator"
    interface = RequestInterface(family=FAMILY)

    class Item(APIResponseItem):
        def __init__(self, response: dict) -> None:
            super().__init__(response)

            if ("data" in response and response["data"] and
                    len(response["data"]) > 0):
                data_item = response["data"][0]
                self.status_code = data_item.get("statusCode", 200)
                self.audioform_id = data_item.get("audioformId", "")
                self.audioform = data_item.get("audioform", {})
            else:
                self.status_code = 200
                self.audioform_id = ""
                self.audioform = {}

    @staticmethod
    def create(
        brief: Optional[Dict[str, Any]] = None,
        file_id: Optional[str] = None,
        num_ads: int = 3,
    ) -> "CreativeBrief.Item":
        """
        Create a new creative brief request.

        Args:
            brief: The creative brief configuration object containing:
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

        Returns:
            CreativeBrief.Item: Response containing audioformId and status

        Raises:
            Exception: If neither brief nor file_id is provided,
                or both are provided
        """
        if brief and file_id:
            raise Exception(
                "Either brief or file_id should be provided, not both"
            )
        if not brief and not file_id:
            raise Exception("Either brief or file_id must be provided")

        body: Dict[str, Any] = {"numAds": num_ads}

        if brief:
            body["brief"] = brief
        else:
            body["fileId"] = file_id  # API uses 'fileId', not 'file_id'

        r = CreativeBrief.interface.send_request(
            rtype=RequestTypes.POST, route="brief", json=body
        )
        return CreativeBrief.Item(r)
