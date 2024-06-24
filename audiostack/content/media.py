import os
from typing import Any

from audiostack.helpers.api_item import APIResponseItem
from audiostack.helpers.api_list import APIResponseList
from audiostack.helpers.request_interface import RequestInterface
from audiostack.helpers.request_types import RequestTypes


class Media:
    FAMILY = "content"
    interface = RequestInterface(family=FAMILY)

    class Item(APIResponseItem):
        def __init__(self, response: dict) -> None:
            super().__init__(response)

            self.mediaId = self.data["mediaId"]
            self.tags = self.data["tags"]
            self.filename = self.data["filename"]

        def delete(self) -> APIResponseItem:
            return Media.delete(self.mediaId)

    class List(APIResponseList):
        def __init__(self, response: dict, list_type: str) -> None:
            super().__init__(response, list_type)

        def resolve_item(self, list_type: str, item: Any) -> "Media.Item":
            if list_type == "mediaFiles":
                return Media.Item({"data": item})
            else:
                raise Exception()

    @staticmethod
    def create(filePath: str) -> Item:
        if not os.path.isfile(filePath):
            raise Exception("Supplied file does not exist")

        name = filePath.rpartition("/")[2]

        r = Media.interface.send_request(
            rtype=RequestTypes.POST,
            route="media/create-upload-url",
            json={"fileName": name},
        )
        response = APIResponseItem(r)
        url = response.data["fileUploadUrl"]
        mediaId = response.data["mediaId"]

        Media.interface.send_upload_request(local_path=filePath, upload_url=url)
        return Media.get(mediaId)

    @staticmethod
    def get(mediaId: str) -> Item:
        r = Media.interface.send_request(
            rtype=RequestTypes.GET, route="media", path_parameters=mediaId
        )
        return Media.Item(r)

    @staticmethod
    def delete(mediaId: str) -> APIResponseItem:
        r = Media.interface.send_request(
            rtype=RequestTypes.DELETE, route="media", path_parameters=mediaId
        )
        return APIResponseItem(r)

    @staticmethod
    def list() -> List:
        r = Media.interface.send_request(rtype=RequestTypes.GET, route="media")
        return Media.List(r, list_type="mediaFiles")
