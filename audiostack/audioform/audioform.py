import time
from typing import Any, Dict

from audiostack import TIMEOUT_THRESHOLD_S
from audiostack.helpers.api_item import APIResponseItem
from audiostack.helpers.request_interface import RequestInterface
from audiostack.helpers.request_types import RequestTypes


class Audioform:
    FAMILY = "audioforms"
    interface = RequestInterface(family=FAMILY)

    class Item(APIResponseItem):
        def __init__(self, response: dict) -> None:
            super().__init__(response)

            if "statusCode" in response:
                self.status_code = response["statusCode"]

            if "data" in response and response["data"]:
                # Standard response with data field
                self.audioform_id = response["data"].get("audioformId", "")
                self.audioform = response["data"].get("audioform", {})
                self.result = response["data"].get("result", {})
                self._errors = response["data"].get("errors", [])
            elif "audioformId" in response:
                # In-progress response with audioformId directly in response
                self.audioform_id = response.get("audioformId", "")
                self.audioform = {}
                self.result = {}
                self._errors = []
            else:
                # Error response or malformed response
                self.audioform_id = ""
                self.audioform = {}
                self.result = {}
                self._errors = response.get("errors", [])

        def get(
            self,
            version: str = "2",
            wait: bool = True,
            timeoutThreshold: int = TIMEOUT_THRESHOLD_S,
        ) -> "Audioform.Item":
            """
            Get the current audioform with updated status and result.

            Args:
                version: Audioform version ("2","1" or "0.0.1", default: "2")
                wait: Whether to poll until status changes from 202 to 200
                timeoutThreshold: Maximum time to wait for completion in seconds

            Returns:
                Audioform.Item: Updated audioform with current status and result
            """
            return Audioform.get(self.audioform_id, version, wait, timeoutThreshold)

        @property
        def is_success(self) -> bool:
            """Check if the audioform was successfully processed"""
            return self.status_code == 200 and not self._errors

        @property
        def is_failed(self) -> bool:
            """Check if the audioform processing failed"""
            return self.status_code == 200 and bool(self._errors)

        @property
        def is_in_progress(self) -> bool:
            """Check if the audioform is still being processed"""
            return self.status_code == 202

        @property
        def errors(self) -> str:
            """Get error message if processing failed"""
            if self._errors:
                return "; ".join(self._errors)
            return ""

    @staticmethod
    def create(audioform: Dict[str, Any]) -> "Audioform.Item":
        """
        Create a new audioform build request.

        Args:
            audioform: The audioform configuration object containing:
                - header: Header configuration (must include version field)
                - assets: Asset configuration
                - production: Production settings (e.g., masteringPreset)
                - delivery: Delivery settings (e.g., loudnessPreset,
                  encoderPreset)

        Returns:
            Audioform.Item: Response containing audioform_id and status
        """
        body = {"audioform": audioform}

        r = Audioform.interface.send_request(
            rtype=RequestTypes.POST, route="", json=body
        )

        return Audioform.Item(r)

    @staticmethod
    def get(
        audioform_id: str,
        version: str = "2",
        wait: bool = True,
        timeoutThreshold: int = TIMEOUT_THRESHOLD_S,
    ) -> "Audioform.Item":
        """
        Get the status and result of an audioform build.

        Args:
            audioform_id: The unique identifier for the audioform
            version: Audioform version ("2", "1" or "0.0.1", default: "2")
                Service will convert stored audioform to requested version
            wait: Whether to poll until status changes from 202 to 200
            timeoutThreshold: Maximum time to wait for completion in seconds

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

        if wait and r.get("statusCode") == 202:
            start = time.time()

            while r.get("statusCode") == 202:
                print("Audioform build in progress, please wait...")
                r = Audioform.interface.send_request(
                    rtype=RequestTypes.GET,
                    route="",
                    path_parameters=audioform_id,
                    headers=headers,
                )

                if time.time() - start >= timeoutThreshold:
                    raise TimeoutError(
                        f"Audioform polling timed out after "
                        f"{timeoutThreshold} seconds. Please contact us for "
                        f"support. AudioformId: {audioform_id}"
                    )

                time.sleep(0.05)

        return Audioform.Item(r)
