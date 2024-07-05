from time import sleep
from typing import Optional

from audiostack.helpers.api_item import APIResponseItem
from audiostack.helpers.api_list import APIResponseList
from audiostack.helpers.request_interface import RequestInterface
from audiostack.helpers.request_types import RequestTypes


class STS:
    interface = RequestInterface(family="speech/sts")

    class StsVoiceItem(APIResponseItem):
        def __init__(self, response: dict) -> None:
            super().__init__(response)
            self.provider = self.data["provider"]
            self.alias = self.data["alias"]
            self.language = self.data["language"]
            self.languageCode = self.data["languageCode"]

    class StsVoiceList(APIResponseList):
        def __init__(self, response: dict, list_type: str) -> None:
            super().__init__(response, list_type)

        def resolve_item(self, list_type: str, x: int) -> APIResponseItem:
            return self.data[list_type][x]

    class FailedPipeline(Exception):
        pass

    class FailedStatusFetch(Exception):
        pass

    class PipelineInProgressItem(APIResponseItem):
        def __init__(self, response: dict) -> None:
            super().__init__(response)
            self.pipelineId = self.data["pipelineId"]

    class PipelineFinishedItem(APIResponseItem):
        def __init__(self, response: dict) -> None:
            super().__init__(response)
            self.pipelineId = self.data["pipelineId"]
            self.newFileIds = self.data["results"]["newFileIds"]
            self.inputFileIds = self.data["results"]["inputFileIds"]
            self.replacedFileIds = self.data["results"]["replacedFileIds"]

    @staticmethod
    def voices() -> APIResponseList:
        r = STS.interface.send_request(rtype=RequestTypes.GET, route="voices")
        return STS.StsVoiceList(r, list_type="voices")

    @staticmethod
    def create(
        alias: str, fileId: str, newFilePath: Optional[str] = None
    ) -> PipelineInProgressItem:
        body = {"alias": alias, "fileId": fileId}
        if newFilePath:
            body["newFilePath"] = newFilePath
        r = STS.interface.send_request(rtype=RequestTypes.POST, route="", json=body)
        item = STS.PipelineInProgressItem(r)
        return item

    @staticmethod
    def get(pipelineId: str) -> PipelineFinishedItem:
        r = STS.interface.send_request(
            rtype=RequestTypes.GET, route="", path_parameters=pipelineId
        )

        if r["data"]["status"] in [200, 202]:
            return STS._poll(r, pipelineId)
        else:
            body = r["data"]["body"]
            raise STS.FailedStatusFetch(f"Failed to fetch pipeline with error: {body}")

    @staticmethod
    def _poll(r: dict, pipelineId: str) -> PipelineFinishedItem:
        pipeline_status_code = r["data"]["status"]
        while pipeline_status_code == 202:
            print("Waiting for pipeline to complete (0.5 seconds)...")
            sleep(0.5)
            r = STS.interface.send_request(
                rtype=RequestTypes.GET, route="", path_parameters=pipelineId
            )
            pipeline_status_code = r["data"]["status"]

        status = r.get("data", {}).get("status", 200)
        if status >= 400:
            msg = r.get("data", {}).get("message")
            errors = r.get("data", {}).get("errors")
            raise STS.FailedPipeline(
                "pipeline failed: ", msg, "errors are as follows: ", ",".join(errors)
            )

        return STS.PipelineFinishedItem(r)
