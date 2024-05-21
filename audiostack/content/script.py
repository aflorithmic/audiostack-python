from typing import Any

from audiostack.helpers.api_item import APIResponseItem
from audiostack.helpers.api_list import APIResponseList
from audiostack.helpers.request_interface import RequestInterface
from audiostack.helpers.request_types import RequestTypes


class Script:
    FAMILY = "content"
    interface = RequestInterface(family=FAMILY)

    class Item(APIResponseItem):
        def __init__(self, response: dict) -> None:
            super().__init__(response)

            self.scriptId = self.data["scriptId"]
            self.projectName = self.data["projectName"]
            self.moduleName = self.data["moduleName"]
            self.scriptName = self.data["scriptName"]
            self.scriptText = self.data["scriptText"]

        def update(self, scriptText: str) -> "Script.Item":
            return Script.update(scriptId=self.scriptId, scriptText=scriptText)

        def delete(self) -> APIResponseItem:
            return Script.delete(self.scriptId)

    class List(APIResponseList):
        def __init__(self, response: dict, list_type: str) -> None:
            super().__init__(response, list_type)

        def resolve_item(self, list_type: str, item: Any) -> "Script.Item":
            if list_type == "scripts":
                return Script.Item({"data": item})
            else:
                raise Exception()

    @staticmethod
    def create(
        scriptText: str,
        projectName: str = "",
        moduleName: str = "",
        scriptName: str = "",
        metadata: dict = {},
    ) -> Item:
        body = {
            "scriptText": scriptText,
            "projectName": projectName,
            "moduleName": moduleName,
            "scriptName": scriptName,
            "metadata": metadata,
        }

        r = Script.interface.send_request(
            rtype=RequestTypes.POST, route="script", json=body
        )
        return Script.Item(r)

    @staticmethod
    def generate_advert(
        product_name: str,
        product_description: str,
        mood: str = "",
        tone: str = "",
        thirdPerson: bool = True,
        adLength: int = 30,
    ) -> APIResponseItem:
        body = {
            "productName": product_name,
            "productDescription": product_description,
            "mood": mood,
            "tone": tone,
            "thirdPerson": thirdPerson,
            "adLength": adLength,
        }

        r = Script.interface.send_request(
            rtype=RequestTypes.POST, route="generate/advert", json=body
        )
        return APIResponseItem(r)

    @staticmethod
    def get(scriptId: str, version: str = "", previewWithVoice: str = "") -> Item:
        path_params = f"{scriptId}/{version}" if version else scriptId
        if previewWithVoice:
            query_params = {
                "preview": bool(previewWithVoice),
                "voice": previewWithVoice,
            }
        else:
            query_params = {}

        r = Script.interface.send_request(
            rtype=RequestTypes.GET,
            route="script",
            path_parameters=path_params,
            query_parameters=query_params,
        )
        return Script.Item(r)

    @staticmethod
    def delete(scriptId: str, version: str = "") -> APIResponseItem:
        path_params = f"{scriptId}/{version}" if version else scriptId
        r = Script.interface.send_request(
            rtype=RequestTypes.DELETE, route="script", path_parameters=path_params
        )
        return APIResponseItem(r)

    @staticmethod
    def update(scriptId: str, scriptText: str, version: str = "") -> Item:
        body = {"scriptId": scriptId, "scriptText": scriptText, "version": version}
        r = Script.interface.send_request(
            rtype=RequestTypes.PUT, json=body, route="script"
        )
        return Script.Item(r)

    @staticmethod
    def list(
        projectName: str = "",
        moduleName: str = "",
        scriptName: str = "",
        scriptId: str = "",
    ) -> List:
        query_params = {
            "projectName": projectName,
            "moduleName": moduleName,
            "scriptName": scriptName,
            "scriptId": scriptId,
        }
        r = Script.interface.send_request(
            rtype=RequestTypes.GET, route="scripts", query_parameters=query_params
        )
        return Script.List(r, list_type="scripts")
