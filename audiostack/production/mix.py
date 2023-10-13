from audiostack.helpers.request_interface import RequestInterface
from audiostack.helpers.request_types import RequestTypes
from audiostack.helpers.api_item import APIResponseItem
from audiostack.helpers.api_list import APIResponseList


class Mix:
    interface = RequestInterface(family="production")

    class Item(APIResponseItem):
        def __init__(self, response) -> None:
            super().__init__(response)
            self.productionId = self.data["productionId"]

        def download(self, fileName="", path="./") -> None:
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

        def delete(self):
            return Mix.delete(self.productionId)

    class List(APIResponseList):
        def __init__(self, response, list_type) -> None:
            super().__init__(response, list_type)

        def resolve_item(self, list_type, item):
            if list_type == "productionIds":
                return Mix.Item({"data": item})
            elif list_type == "presets":
                return

            else:
                raise Exception()

    @staticmethod
    def create(
        speechId="",
        speechItem=None,
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
        soundLayer: str = "default"
    ) -> Item:
        if speechId and speechItem:
            raise Exception("speechId or scriptItem should be supplied not both")
        if not (speechId or speechItem):
            raise Exception("speechId or scriptItem should be supplied")
        if speechItem:
            speechId = speechItem.speechId

        if not isinstance(soundTemplate, str):
            raise Exception("soundTemplate argument should be a string")
        if not isinstance(masteringPreset, str):
            raise Exception("masteringPreset should be a string")
        

        body = {
            "speechId": speechId,
            "soundTemplate": soundTemplate,
            "mediaFiles": mediaFiles,
            "fxFiles": fxFiles,
            "sectionProperties": sectionProperties,
            "timelineProperties": timelineProperties,
            "soundLayer": soundLayer,
            "masteringPreset": masteringPreset,
            "public": public,
            "exportSettings" : exportSettings,
            "strictValidation" : strictValidation
        }
        if validate:
            r = Mix.interface.send_request(rtype=RequestTypes.POST, route="validate", json=body)
        else:
            r = Mix.interface.send_request(rtype=RequestTypes.POST, route="mix", json=body)
            
        while r["statusCode"] == 202:
            print("Response in progress please wait...")
            r = Mix.interface.send_request(
                rtype=RequestTypes.GET, route="mix", path_parameters=r["data"]["productionId"]
            )
        
        return Mix.Item(r)

    @staticmethod
    def get(productionId: str) -> Item:
        r = Mix.interface.send_request(
            rtype=RequestTypes.GET, route="mix", path_parameters=productionId
        )
        return Mix.Item(r)

    @staticmethod
    def delete(productionId: str) -> str:
        r = Mix.interface.send_request(
            rtype=RequestTypes.DELETE, route="mix", path_parameters=productionId
        )
        return APIResponseItem(r)

    @staticmethod
    def list(
        projectName="", moduleName: str = "", scriptName: str = "", scriptId: str = ""
    ) -> list:
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
    def list_presets() -> Item:
        r = Mix.interface.send_request(
            rtype=RequestTypes.GET, route="mix/presets", path_parameters=""
        )
        return Mix.List(response=r, list_type="presets")
