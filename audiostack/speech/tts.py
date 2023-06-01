from audiostack.helpers.request_interface import RequestInterface
from audiostack.helpers.request_types import RequestTypes
from audiostack.helpers.api_item import APIResponseItem
from audiostack.helpers.api_list import APIResponseList


class TTS:
    interface = RequestInterface(family="speech")

    class Item(APIResponseItem):
        def __init__(self, response) -> None:
            super().__init__(response)
            self.speechId = self.data["speechId"]

        def download(self, autoName=False, fileName="", path="./") -> None:
            sections = self.data["sections"]
            for i, s in enumerate(sections):
                if autoName:
                    full_name = ""
                    for k, val in s["audience"].items():
                        full_name += f"{k}={val}~"

                    full_name = full_name[:-1] + ".wav"
                else:
                    if not fileName:
                        full_name = s["sectionName"] + ".wav"
                    else:
                        full_name = f"{fileName}_{i+1}_of_{len(sections)}.wav"
                RequestInterface.download_url(
                    s["url"], destination=path, name=full_name
                )

        def delete(self):
            return TTS.delete(self.speechId)

    class List(APIResponseList):
        def __init__(self, response, list_type) -> None:
            super().__init__(response, list_type)

        def resolve_item(self, list_type, item):
            if list_type == "speechIds":
                return TTS.Item({"data": item})
            else:
                raise Exception()

    @staticmethod
    def create(
        scriptId="",
        scriptItem=None,
        voice: str = "",
        speed: float = 1.0,
        silencePadding: str = "",
        effect: str = "",
        audience: dict = {},
        sections: dict = {},
        useDictionary: bool = False,
        useTextNormalizer: bool = False,
        public: bool = False,
        sync: bool = True,
    ) -> Item:
        if scriptId and scriptItem:
            raise Exception("scriptId or scriptItem should be supplied not both")
        if not (scriptId or scriptItem):
            raise Exception("scriptId or scriptItem should be supplied")

        if scriptItem:
            scriptId = scriptItem.scriptId

        if not isinstance(voice, str):
            raise Exception("voice argument should be a string")
        if not isinstance(effect, str):
            raise Exception("effect argument should be a string")
        if not isinstance(silencePadding, str):
            raise Exception("silencePadding argument should be a string")
        if not isinstance(useDictionary, bool):
            raise Exception("useDictionary argument should be a boolean")
        if not isinstance(useTextNormalizer, bool):
            raise Exception("useTextNormaliser argument should be a boolean")

        body = {
            "scriptId": scriptId,
            "voice": voice,
            "speed": speed,
            "silencePadding": silencePadding,
            "effect": effect,
            "audience": audience,
            "sections": sections,
            "useDictionary": useDictionary,
            "useTextNormalizer": useTextNormalizer,
            "public": public,
            "sync": sync,
        }

        r = TTS.interface.send_request(rtype=RequestTypes.POST, route="tts", json=body)
        while r["statusCode"] == 202:
            print("Response in progress please wait...")
            r = TTS.interface.send_request(
                rtype=RequestTypes.GET, route="tts", path_parameters=r["data"]["speechId"]   
            )
            
        return TTS.Item(r)

    @staticmethod
    def get(speechId: str) -> Item:
        r = TTS.interface.send_request(
            rtype=RequestTypes.GET, route="tts", path_parameters=speechId
        )
        return TTS.Item(r)

    @staticmethod
    def delete(speechId: str) -> str:
        r = TTS.interface.send_request(
            rtype=RequestTypes.DELETE, route="tts", path_parameters=speechId
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
        r = TTS.interface.send_request(
            rtype=RequestTypes.GET, route="tts", query_parameters=query_params
        )
        return TTS.List(r, list_type="speechIds")
