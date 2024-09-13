from typing import Any, Optional

from audiostack.helpers.api_item import APIResponseItem
from audiostack.helpers.api_list import APIResponseList
from audiostack.helpers.request_interface import RequestInterface
from audiostack.helpers.request_types import RequestTypes


class TTS:
    interface = RequestInterface(family="speech")

    class Item(APIResponseItem):
        def __init__(self, response: dict) -> None:
            super().__init__(response)
            self.speechId = self.data["speechId"]

        def download(
            self, autoName: bool = False, fileName: str = "", path: str = "./"
        ) -> None:
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

        def delete(self) -> APIResponseItem:
            return TTS.delete(self.speechId)

    class BytesItem(APIResponseItem):
        def __init__(self, response: dict) -> None:
            super().__init__(response)
            self.bytes = response["bytes"]

        # def download(self, autoName=False, fileName="default", path="./") -> None:
        #     with open("")

    class List(APIResponseList):
        def __init__(self, response: dict, list_type: Any) -> None:
            super().__init__(response, list_type)

        def resolve_item(self, list_type: str, item: Any) -> "TTS.Item":
            if list_type == "speechIds":
                return TTS.Item({"data": item})
            else:
                raise Exception()

    class Section:
        @staticmethod
        def create(
            sectionToProduce: Any,
            scriptId: str = "",
            scriptItem: Optional[Any] = None,
            voice: str = "",
            speed: float = 1.0,
            silencePadding: str = "",
            audience: dict = {},
            sections: dict = {},
            voiceIntelligence: bool = False,
            public: bool = False,
            sync: bool = True,
            useCache: bool = True,
            useDenoiser: bool = False,
            useAutofix: bool = False,
        ) -> "TTS.Item":
            # (start) no modify
            route = "tts/section"
            return TTS._create(**locals())
            # (end) modify

    @staticmethod
    def preview(text: str, voice: str) -> "TTS.BytesItem":
        body = {"text": text, "voice": voice}
        r = TTS.interface.send_request(
            rtype=RequestTypes.POST, route="tts/preview", json=body
        )
        return TTS.BytesItem(r)

    @staticmethod
    def reduce(speechId: str, targetLength: str, sectionId: str = "") -> "TTS.Item":
        body = {
            "speechId": speechId,
            "targetLength": targetLength,
            "sectionId": sectionId,
        }
        r = TTS.interface.send_request(
            rtype=RequestTypes.POST, route="tts/reduce", json=body
        )
        print(r)
        return TTS.Item(r)

    @staticmethod
    def remove_padding(
        speechId: str,
        minSilenceDuration: float = 1.5,
        silenceThreshold: float = 0.001,
        position: str = "end",
        sectionId: str = "",
    ) -> "TTS.Item":
        body = {
            "speechId": speechId,
            "minSilenceDuration": minSilenceDuration,
            "silenceThreshold": silenceThreshold,
            "position": position,
            "sectionId": sectionId,
        }
        r = TTS.interface.send_request(
            rtype=RequestTypes.POST, route="tts/remove_padding", json=body
        )
        print(r)
        return TTS.Item(r)

    @staticmethod
    def annotate(
        speechId: str,
        scriptReference: str = "",
        languageCode: str = "",
        continuousRecognition: bool = False,
    ) -> dict:
        body = {
            "speechId": speechId,
            "scriptReference": scriptReference,
            "language_code": languageCode,
            "continuous_recognition": continuousRecognition,
        }
        r = TTS.interface.send_request(
            rtype=RequestTypes.POST, route="tts/annotate", json=body
        )
        print(r)
        return r

    @staticmethod
    def create(
        scriptId: str = "",
        scriptItem: Optional[Any] = None,
        voice: str = "",
        speed: float = 1.0,
        silencePadding: str = "",
        audience: dict = {},
        sections: dict = {},
        voiceIntelligence: bool = False,
        public: bool = False,
        sync: bool = True,
        useCache: bool = True,
        useDenoiser: bool = False,
        useAutofix: bool = False,
    ) -> "TTS.Item":
        # (start) no modify
        route = "tts"
        return TTS._create(**locals())
        # (end) modify

    @staticmethod
    def get(speechId: str, public: bool = False) -> "TTS.Item":
        r = TTS.interface.send_request(
            rtype=RequestTypes.GET,
            route="tts",
            path_parameters=speechId,
            query_parameters={"public": public},
        )
        return TTS.Item(r)

    @staticmethod
    def delete(speechId: str) -> APIResponseItem:
        r = TTS.interface.send_request(
            rtype=RequestTypes.DELETE, route="tts", path_parameters=speechId
        )
        return APIResponseItem(r)

    @staticmethod
    def list(
        projectName: str = "",
        moduleName: str = "",
        scriptName: str = "",
        scriptId: str = "",
    ) -> "TTS.List":
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

    @staticmethod
    def _create(
        route: str,
        scriptId: str = "",
        scriptItem: Optional[Any] = None,
        voice: str = "",
        speed: float = 1.0,
        silencePadding: str = "",
        audience: dict = {},
        sections: dict = {},
        voiceIntelligence: bool = False,
        public: bool = False,
        sync: bool = True,
        useAutofix: bool = False,
        sectionToProduce: str = "",
        useCache: bool = True,
        useDenoiser: bool = False,
    ) -> "TTS.Item":
        if scriptId and scriptItem:
            raise Exception("scriptId or scriptItem should be supplied not both")
        if not (scriptId or scriptItem):
            raise Exception("scriptId or scriptItem should be supplied")

        if scriptItem:
            scriptId = scriptItem.scriptId

        if not isinstance(voice, str):
            raise Exception("voice argument should be a string")
        if not isinstance(silencePadding, str):
            raise Exception("silencePadding argument should be a string")

        body = {
            "scriptId": scriptId,
            "voice": voice,
            "speed": speed,
            "silencePadding": silencePadding,
            "audience": audience,
            "sections": sections,
            "voiceIntelligence": voiceIntelligence,
            "public": public,
            "sync": sync,
            "useCache": useCache,
            "useDenoiser": useDenoiser,
            "useAutofix": useAutofix,
        }
        if sectionToProduce:
            body["sectionToProduce"] = sectionToProduce

        r = TTS.interface.send_request(rtype=RequestTypes.POST, route="tts", json=body)
        while r["statusCode"] == 202:
            print("Response in progress please wait...")
            r = TTS.interface.send_request(
                rtype=RequestTypes.GET,
                route=route,
                path_parameters=r["data"]["speechId"],
                query_parameters={"public": public},
            )

        return TTS.Item(r)
