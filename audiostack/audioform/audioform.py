from typing import Any, Dict

from audiostack.helpers.api_item import APIResponseItem
from audiostack.helpers.request_interface import RequestInterface
from audiostack.helpers.request_types import RequestTypes


class Audioform:
    FAMILY = "audioforms"
    interface = RequestInterface(family=FAMILY)

    class Item(APIResponseItem):
        def __init__(self, response: dict) -> None:
            super().__init__(response)

            if "data" in response and response["data"]:
                self.audioform_id = response["data"].get("audioformId", "")
                self.status_code = response["data"].get("statusCode", 200)
                self.audioform = response["data"].get("audioform", {})
                self.result = response["data"].get("result", {})
            else:
                self.audioform_id = ""
                self.status_code = 200
                self.audioform = {}
                self.result = {}

        def get(self) -> "Audioform.Item":
            """Get the current audioform status"""
            return Audioform.get(self.audioform_id)

    @staticmethod
    def create(
        audioform: Dict[str, Any]
    ) -> "Audioform.Item":
        """
        Create a new audioform build request.

        Args:
            audioform: The audioform configuration object containing:
                - header: Optional header configuration
                  (version will be added here)
                - assets: Asset configuration
                - production: Production settings (e.g., masteringPreset)
                - delivery: Delivery settings (e.g., loudnessPreset,
                  encoderPreset)
            version: Audioform version ("1" or "0.0.1", default: "1")

        Returns:
            Audioform.Item: Response containing audioform_id and status
        """
        # Add version to audioform header
        audioform_with_version = audioform.copy()
        if "header" not in audioform_with_version:
            audioform_with_version["header"] = {}
        audioform_with_version["header"]["version"] = version

        body = {"audioform": audioform_with_version}

        r = Audioform.interface.send_request(
            rtype=RequestTypes.POST, route="", json=body
        )
        return Audioform.Item(r)

    @staticmethod
    def get(audioform_id: str, version: str = "1") -> "Audioform.Item":
        """
        Get the status and result of an audioform build.

        Args:
            audioform_id: The unique identifier for the audioform
            version: Audioform version ("1" or "0.0.1", default: "1")

        Returns:
            Audioform.Item: Response containing build status and result
        """
        headers = {"version": version}

        r = Audioform.interface.send_request(
            rtype=RequestTypes.GET,
            route="",
            path_parameters=audioform_id,
            headers=headers,
        )
        return Audioform.Item(r)
