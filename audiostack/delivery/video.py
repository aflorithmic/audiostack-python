from typing import Any, Optional

from audiostack.helpers.api_item import APIResponseItem
from audiostack.helpers.request_interface import RequestInterface
from audiostack.helpers.request_types import RequestTypes
from audiostack.production.suite import Suite


class Video:
    interface = RequestInterface(family="delivery")

    class Item(APIResponseItem):
        def __init__(self, response: dict) -> None:
            super().__init__(response)
            self.url = self.data["url"]
            self.format = self.data.get("format", "mp4")

        def download(self, fileName: str = "default", path: str = "./") -> None:
            full_name = f"{fileName}.{self.format}"
            RequestInterface.download_url(self.url, destination=path, name=full_name)

    @staticmethod
    def create_from_production_and_image(
        productionId: str = "",
        productionItem: Optional[Any] = None,
        public: bool = False,
    ) -> Item:
        if productionId and productionItem:
            raise Exception(
                "productionId or productionItem should be supplied not both"
            )
        if not (productionId or productionItem):
            raise Exception("productionId or productionItem should be supplied")

        if productionItem:
            try:
                productionId = productionItem.productionId
            except Exception:
                raise Exception(
                    "supplied productionItem is missing an attribute, productionItem should be type object and a response from Production.Mix"
                )
        elif productionId:
            if not isinstance(productionId, str):
                raise Exception("supplied productionId should be a uuid string.")
        body = {
            "productionId": productionId,
            "public": public,
        }
        r = Video.interface.send_request(
            rtype=RequestTypes.POST, route="video", json=body
        )
        retries = 0
        max_retries = 30
        while r["statusCode"] == 202 and retries < max_retries:
            print("Response in progress please wait...")
            videoId = r["data"]["videoId"]
            r = Video.interface.send_request(
                rtype=RequestTypes.GET, route="video", path_parameters=videoId
            )
            retries += 1
        return Video.Item(r)

    @staticmethod
    def create_from_production_and_video(
        productionId: str = "",
        productionItem: Optional[Any] = None,
        videoFileId: str = "",
        mode: dict = {},
        public: bool = False,
    ) -> Item:
        if productionId and productionItem:
            raise Exception(
                "productionId or productionItem should be supplied not both"
            )
        if not (productionId or productionItem):
            raise Exception("productionId or productionItem should be supplied")

        if productionItem:
            try:
                productionId = productionItem.productionId
            except Exception:
                raise Exception(
                    "supplied productionItem is missing an attribute, productionItem should be type object and a response from Production.Mix"
                )
        elif productionId:
            if not isinstance(productionId, str):
                raise Exception("supplied productionId should be a uuid string.")
        body = {
            "productionId": productionId,
            "public": public,
            "videoFileId": videoFileId,
            "mode": mode,
            "format": "",
        }
        r = Video.interface.send_request(
            rtype=RequestTypes.POST, route="video", json=body
        )
        retries = 0
        max_retries = 30
        while r["statusCode"] == 202 and retries < max_retries:
            print("Response in progress please wait...")
            videoId = r["data"]["videoId"]
            r = Video.interface.send_request(
                rtype=RequestTypes.GET, route="video", path_parameters=videoId
            )
            retries += 1
        return Video.Item(r)

    @staticmethod
    def create_from_file_and_video(
        fileId: str = "",
        videoFileId: str = "",
        mode: dict = {},
    ) -> Item:
        interface = RequestInterface(family="production")

        if fileId and not videoFileId:
            raise Exception(
                "if videoFileId is supplied, fileId should be supplied as well"
            )

        body = {
            "fileId": fileId,
            "videoFileId": videoFileId,
            "public": False,
            "outputFormat": "",
            "mode": mode,
        }

        r = interface.send_request(
            rtype=RequestTypes.POST, route="suite/file_to_video", json=body
        )

        item = Suite.PipelineInProgressItem(r)
        return Video.Item(_poll_video(r, item.pipelineId))

    @staticmethod
    def create_from_file_and_image(fileId: str = "") -> Item:
        interface = RequestInterface(family="production")

        body = {
            "fileId": fileId,
            "public": False,
            "outputFormat": "mp4",
            "mode": {"setting": "default"},
        }

        r = interface.send_request(
            rtype=RequestTypes.POST, route="suite/file_to_video", json=body
        )

        item = Suite.PipelineInProgressItem(r)
        return Video.Item(_poll_video(r, item.pipelineId))


def _poll_video(r: dict, pipelineId: str) -> dict:
    while r["statusCode"] == 202:
        interface = RequestInterface(family="production")
        print("Response in progress please wait...")
        r = interface.send_request(
            rtype=RequestTypes.GET,
            route="suite/videopipeline",
            path_parameters=pipelineId,
        )
    status = r.get("data", {}).get("status", 200)
    if status > 400:
        msg = r.get("data", {}).get("message")
        errors = r.get("data", {}).get("errors")
        raise Suite.FailedPipeline(
            "pipeline failed: ", msg, "errors are as follows: ", ",".join(errors)
        )

    return r
