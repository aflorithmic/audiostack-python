import time
from typing import Any, Dict

from audiostack import TIMEOUT_THRESHOLD_STORY_S
from audiostack.helpers.api_item import APIResponseItem
from audiostack.helpers.request_interface import RequestInterface
from audiostack.helpers.request_types import RequestTypes


class Story:
    FAMILY = "creator"
    interface = RequestInterface(family=FAMILY)

    class Item(APIResponseItem):
        def __init__(self, response: dict) -> None:
            super().__init__(response)

            data = response.get("data", {})
            self.story_id = data.get("storyId", "")
            if not self.story_id:
                raise Exception("Story ID missing")

            self.story_build_status_code = data.get("statusCode", None)

            self.story_result = {}
            self.audioforms = []
            self._errors = ""

            if (
                self.story_build_status_code != 200
                and self.story_build_status_code != 202
            ):
                """Retrieve the error message if story build failed"""
                self._errors = data.get("message", "")
            else:
                """Standard response for successful story builds"""
                self.story_result = data.get("storyResult", {})
                self.audioforms = data.get("audioforms", [])

        @property
        def is_success(self) -> bool:
            """Check if the story was built successfully"""
            if self.story_build_status_code is None:
                return False
            return 200 <= self.story_build_status_code < 300 and not self._errors

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
        story_id: str, timeoutThreshold: int = TIMEOUT_THRESHOLD_STORY_S
    ) -> "Story.Item":
        """
        Get the result of a story build.

        Args:
            story_id: Unique identifier for the story
            timeoutThreshold: Maximum time to wait for completion in seconds

        Returns:
            Story.Item: Response containing story status and result
        """
        r = Story.interface.send_request(
            rtype=RequestTypes.GET,
            route="story",
            path_parameters=story_id,
        )

        if r.get("statusCode") == 202:
            start = time.time()

            print("Story build starting...")
            time.sleep(7)

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

                time.sleep(7)

            return Story.Item(r)

        return Story.Item(r)
