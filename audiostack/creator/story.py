import time
from typing import Any, Dict

from audiostack import TIMEOUT_THRESHOLD_S
from audiostack.helpers.api_item import APIResponseItem
from audiostack.helpers.request_interface import RequestInterface
from audiostack.helpers.request_types import RequestTypes


class Story:
    FAMILY = "creator"
    interface = RequestInterface(family=FAMILY)

    class Item(APIResponseItem):
        def __init__(self, response: dict) -> None:
            super().__init__(response)

            self.story_id = ""
            self.audioform_status_code = None
            self.audioform_ids = []
            self.audioforms = {}
            self.results = {}
            self._errors = ""

            data = response.get("data", {})

            if "storyId" in data and data["storyId"]:
                self.story_id = data.get("storyId")

            if "statusCode" in data and data["statusCode"]:
                self.audioform_status_code = data.get("statusCode")

            if self.audioform_status_code != 200:
                """Retrieve the error message if story build failed"""
                self._errors = data.get("message", "")

            else:
                """Standard response for successful story builds"""
                for audioform in data.get("audioforms", []):
                    audioform_id = audioform.get("header", {}).get("audioformId", "")

                    self.audioform_ids.append(audioform_id)
                    self.audioforms[audioform_id] = audioform
                    self.results[audioform_id] = audioform.get("delivery", {})

        @property
        def is_success(self) -> bool:
            """Check if the story was built successfully"""
            if self.audioform_status_code is None:
                return False
            return 200 <= self.audioform_status_code < 300 and not hasattr(self, '_errors')

        @property
        def is_failed(self) -> bool:
            """Check if the story build failed"""
            return self.status_code >= 400 or bool(self._errors)

        @property
        def get_audioform_count(self) -> int:
            """Check the number of generated audioforms for the story"""
            return len(self.audioform_ids)

    @staticmethod
    def create(story: Dict[str, Any]) -> "Story.Item":
        """
        Create a new story build request.

        Args:
            story: The story configuration object containing:
                - title: Title of the story
                - voices: Array of voice configurations
                - sounds: Sound design and sound effect configuration
                - production: Production configurations
                - delivery: Delivery configurations
                - chapters: Desired story structure

        Returns:
            Story.Item: Response containing story_id
        """
        if not isinstance(story, dict):
            raise Exception("Story must be a dictionary")

        body = {"story": story}
        r = Story.interface.send_request(
            rtype=RequestTypes.POST, route="story", json=body
        )

        return Story.Item(r)

    @staticmethod
    def get(
        story_id: str, wait: bool = True, timeoutThreshold: int = TIMEOUT_THRESHOLD_S
    ) -> "Story.Item":
        """
        Get the result of a story build.

        Args:
            story_id: Unique identifier for the story
            wait: Whether to poll until story status changes from 202 to 200
            timeoutThreshold: Maximum time to wait for completion in seconds

        Returns:
            Story.Item: Response containing story status and result
        """
        r = Story.interface.send_request(
            rtype=RequestTypes.GET,
            route="story",
            path_parameters=story_id,
        )

        if wait and r.get("statusCode") == 202:
            start = time.time()
            print(r)

            while r.get("statusCode") == 202:
                print("Story build in progress, please wait...")
                r = Story.interface.send_request(
                    rtype=RequestTypes.GET,
                    route="story",
                    path_parameters=story_id,
                )

                if time.time() - start >= timeoutThreshold:
                    raise TimeoutError(
                        f"Story polling timed out after {time.time() - start:.2f} seconds.\nPlease contact AudioStack for support with StoryId: {story_id}"
                    )

                time.sleep(2)

        return Story.Item(r)
    
if __name__ == "__main__":
    import os
