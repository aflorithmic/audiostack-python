from typing import Any, Optional

from audiostack.helpers.api_item import APIResponseItem
from audiostack.helpers.api_list import APIResponseList
from audiostack.helpers.request_interface import RequestInterface
from audiostack.helpers.request_types import RequestTypes


class Encoder:
    interface = RequestInterface(family="delivery")

    class Item(APIResponseItem):
        def __init__(self, response: dict) -> None:
            super().__init__(response)
            self.url = self.data["url"]
            self.format = self.data["format"]

        def download(self, fileName: str = "default", path: str = "./") -> None:
            full_name = f"{fileName}.{self.format}"
            RequestInterface.download_url(self.url, destination=path, name=full_name)

    class List(APIResponseList):
        def __init__(self, response: dict, list_type: str) -> None:
            super().__init__(response, list_type)

        def resolve_item(self, list_type: str, item: Any) -> "Encoder.Item":
            if list_type == "encodedItems":
                return Encoder.Item({"data": item})
            else:
                raise Exception()

    @staticmethod
    def encode_mix(
        preset: str,
        productionId: str = "",
        productionItem: Optional[Any] = None,
        loudnessPreset: str = "",
        public: bool = False,
        bitRateType: str = "",
        bitRate: Optional[int] = None,
        sampleRate: Optional[int] = None,
        format: str = "",
        bitDepth: Optional[int] = None,
        channels: Optional[int] = None,
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

        if not preset:
            raise Exception(
                "Either a an encoding preset (preset) or a loudness preset (loudnessPreset) should be supplied"
            )

        body = {
            "productionId": productionId,
            "preset": preset,
            "public": public,
            "bitRateType": bitRateType,
            "bitRate": bitRate,
            "sampleRate": sampleRate,
            "format": format,
            "bitDepth": bitDepth,
            "channels": channels,
            "loudnessPreset": loudnessPreset,
        }
        r = Encoder.interface.send_request(
            rtype=RequestTypes.POST, route="encoder", json=body
        )

        while r["statusCode"] == 202:
            print("Response in progress please wait...")
            encoderId = r["data"]["encoderId"]
            r = Encoder.interface.send_request(
                rtype=RequestTypes.GET, route="encoder", path_parameters=encoderId
            )
        return Encoder.Item(r)

    @staticmethod
    def list_presets() -> "Encoder.List":
        r = Encoder.interface.send_request(
            rtype=RequestTypes.GET, route="encoder/presets", path_parameters=""
        )
        return Encoder.List(response=r, list_type="presets")
