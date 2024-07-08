from typing import Any, Optional, Union

from audiostack.helpers.api_item import APIResponseItem
from audiostack.helpers.api_list import APIResponseList
from audiostack.helpers.request_interface import RequestInterface
from audiostack.helpers.request_types import RequestTypes


class Mix:
    interface = RequestInterface(family="production")

    class Item(APIResponseItem):
        def __init__(self, response: dict) -> None:
            super().__init__(response)
            self.productionId = self.data["productionId"]

        def download(self, fileName: str = "", path: str = "./") -> None:
            sections = self.data["files"]
            for i, s in enumerate(sections):
                format = s["format"]
                original_name = s["filename"]

                if not fileName:
                    full_name = f"{original_name}.{format}"
                else:
                    full_name = f"{fileName}_{i}.{format}"

                RequestInterface.download_url(
                    s["url"], destination=path, name=full_name
                )

        def delete(self) -> APIResponseItem:
            return Mix.delete(self.productionId)

    class List(APIResponseList):
        def __init__(self, response: dict, list_type: str) -> None:
            super().__init__(response, list_type)

        def resolve_item(self, list_type: str, item: Any) -> Union["Mix.Item", None]:
            if list_type == "productionIds":
                return Mix.Item({"data": item})
            elif list_type == "presets":
                return None
            else:
                raise Exception()

    @staticmethod
    def create(
        speechId: str = "",
        scriptId: str = "",
        speechItem: Optional[Any] = None,
        soundTemplate: str = "",
        mediaFiles: dict = {},
        fxFiles: dict = {},
        sectionProperties: dict = {},
        timelineProperties: dict = {},
        masteringPreset: str = "",
        public: bool = False,
        exportSettings: dict = {},
        strictValidation: bool = True,
        validate: bool = False,
        sections: dict = {},
        soundLayer: str = "default",
    ) -> Item:
        counts = sum([1 for i in [speechId, scriptId, speechItem] if i])
        if counts != 1:
            raise Exception(
                "only 1 of the following is required; speechId, speechItem, or scriptId"
            )

        if speechItem:
            speechId = speechItem.speechId

        if not isinstance(soundTemplate, str):
            raise Exception("soundTemplate argument should be a string")
        if not isinstance(masteringPreset, str):
            raise Exception("masteringPreset should be a string")
        if not isinstance(sections, dict):
            raise Exception("sections should be a dict")

        body = {
            "soundTemplate": soundTemplate,
            "mediaFiles": mediaFiles,
            "fxFiles": fxFiles,
            "sectionProperties": sectionProperties,
            "timelineProperties": timelineProperties,
            "soundLayer": soundLayer,
            "sections": sections,
            "masteringPreset": masteringPreset,
            "public": public,
            "exportSettings": exportSettings,
            "strictValidation": strictValidation,
        }
        if speechId:
            body["speechId"] = speechId
        elif scriptId:
            body["scriptId"] = scriptId

        if validate:
            r = Mix.interface.send_request(
                rtype=RequestTypes.POST, route="validate", json=body
            )
        else:
            r = Mix.interface.send_request(
                rtype=RequestTypes.POST, route="mix", json=body
            )

        while r["statusCode"] == 202:
            print("Response in progress please wait...")
            r = Mix.interface.send_request(
                rtype=RequestTypes.GET,
                route="mix",
                path_parameters=r["data"]["productionId"],
            )

        return Mix.Item(r)

    @staticmethod
    def get(productionId: str) -> Item:
        r = Mix.interface.send_request(
            rtype=RequestTypes.GET, route="mix", path_parameters=productionId
        )
        return Mix.Item(r)

    @staticmethod
    def delete(productionId: str) -> APIResponseItem:
        r = Mix.interface.send_request(
            rtype=RequestTypes.DELETE, route="mix", path_parameters=productionId
        )
        return APIResponseItem(r)

    @staticmethod
    def list(
        projectName: str = "",
        moduleName: str = "",
        scriptName: str = "",
        scriptId: str = "",
    ) -> "Mix.List":
        query_params = {
            "projectName": projectName,
            "moduleName": moduleName,
            "scriptName": scriptName,
            "scriptId": scriptId,
        }

        r = Mix.interface.send_request(
            rtype=RequestTypes.GET, route="mixes", query_parameters=query_params
        )
        return Mix.List(r, list_type="productionIds")

    @staticmethod
    def list_presets() -> "Mix.List":
        r = Mix.interface.send_request(
            rtype=RequestTypes.GET, route="mix/presets", path_parameters=""
        )
        return Mix.List(response=r, list_type="presets")
