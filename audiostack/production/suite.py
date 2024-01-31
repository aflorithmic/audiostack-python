from audiostack.helpers.request_interface import RequestInterface
from audiostack.helpers.request_types import RequestTypes
from audiostack.helpers.api_item import APIResponseItem
# from audiostack.helpers.api_list import APIResponseList


class Suite:
    interface = RequestInterface(family="production")

    class Item(APIResponseItem):
        def __init__(self, response) -> None:
            super().__init__(response)
    

    @staticmethod
    def evaluate(
        fileId="",
        preset: str = "",
        processes: list = [],
        text: str = "",
        scriptId: str = "",
        language: str = "en-US",
    ) -> Item:
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
            "text": text,
            "scriptId": scriptId,
            "language": language
        }
        
        r = Suite.interface.send_request(rtype=RequestTypes.POST, route="suite/evaluate", json=body)

        while r["statusCode"] != 200 and r["statusCode"] !=404:   # TODO REVISE
            print("Response in progress please wait...")
            r = Suite.interface.send_request(rtype=RequestTypes.POST, route="suite/evaluate", json=body)
            
        return Suite.Item(r)