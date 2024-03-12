from audiostack.helpers.request_interface import RequestInterface
from audiostack.helpers.request_types import RequestTypes
from audiostack.helpers.api_item import APIResponseItem
from audiostack.content.file import File
from typing import List
class Suite:
    interface = RequestInterface(family="production")

    class EvaluationItem(APIResponseItem):
        def __init__(self, response) -> None:
            super().__init__(response)

    class PipelineInProgressItem(APIResponseItem):
        def __init__(self, response) -> None:
            super().__init__(response)
            
            self.pipelineId = self.data["pipelineId"]

    class PipelineFinishedItem(PipelineInProgressItem):
        def __init__(self, response) -> None:
            super().__init__(response)
            self.newFileIds = self.data["results"]["newFileIds"]
            self.inputFileIds = self.data["results"]["inputFileIds"]
            self.replacedFileIds = self.data["results"]["replacedFileIds"]
        
        def convert_new_files_to_items(self) -> List["File.Item"]:
            return [File.get(f["fileId"]) for f in self.newFileIds]
        
        def convert_replaced_files_to_items(self) -> List["File.Item"]:
            return [File.get(f["fileId"]) for f in self.replacedFileIds]
        
    @staticmethod
    def evaluate(
        fileId: str,
        preset: str = "",
        processes: list = [],
        text: str = "",
        scriptId: str = "",
        language: str = "en-US",
    ) -> EvaluationItem:
        if not (fileId):
            raise Exception("fileId should be supplied")
        if text and scriptId:
            raise Exception("either text or scriptId or none should be supplied not both")
        if not isinstance(processes, list):
            raise Exception("processes should be a list")
        if not isinstance(preset, str):
            raise Exception("preset should be a string")

        body = {
            "fileId": fileId,
            "preset": preset,
            "processes": processes,
            "language": language
        }
        if text:
            body["text"] = text
        elif scriptId:
            body["scriptId"] = scriptId
        
        r = Suite.interface.send_request(rtype=RequestTypes.POST, route="suite/evaluate", json=body)

        while r["statusCode"] != 200 and r["statusCode"] !=404:   # TODO REVISE
            print("Response in progress please wait...")
            r = Suite.interface.send_request(rtype=RequestTypes.POST, route="suite/evaluate", json=body)
            
        return Suite.EvaluationItem(r)
    
    @staticmethod
    def separate(fileId: str, wait=True):

        body = {
            "fileId": fileId,
        }
        r = Suite.interface.send_request(rtype=RequestTypes.POST, route="suite/separate", json=body)
        item = Suite.PipelineInProgressItem(r)
        return Suite._poll(r, item.pipelineId) if wait else item
    
    @staticmethod
    def denoise(fileId: str, level: int, wait=True):

        body = {
            "fileId": fileId,
            "level": level
        }
        r = Suite.interface.send_request(rtype=RequestTypes.POST, route="suite/denoise", json=body)
        item = Suite.PipelineInProgressItem(r)
        return Suite._poll(r, item.pipelineId) if wait else item
        

    @staticmethod
    def _poll(r, pipelineId: str):
        while r["statusCode"] == 202:
            r = Suite.interface.send_request(
                rtype=RequestTypes.GET, route="suite/pipeline", path_parameters=pipelineId
            )
        return Suite.PipelineFinishedItem(r)


    @staticmethod
    def get(pipelineId: str):
        r = Suite.interface.send_request(rtype=RequestTypes.GET, route="suite/pipeline", path_parameters=pipelineId)
        return Suite._poll(r, pipelineId)