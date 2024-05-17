from typing import Any

from audiostack.helpers.api_item import APIResponseItem
from audiostack.helpers.api_list import APIResponseList
from audiostack.helpers.request_interface import RequestInterface
from audiostack.helpers.request_types import RequestTypes


class Predict:
    interface = RequestInterface(family="speech/predict")

    class Item(APIResponseItem):
        def __init__(self, response: dict) -> None:
            super().__init__(response)

            self.length = self.data["length"]

    class List(APIResponseList):
        def __init__(self, response: dict, list_type: str) -> None:
            super().__init__(response, list_type)

        def resolve_item(self, list_type: str, item: Any) -> "Predict.Item":
            if list_type == "voices":
                return item
            else:
                raise Exception()

    @staticmethod
    def list() -> "Predict.List":
        r = Predict.interface.send_request(rtype=RequestTypes.GET, route="voices")
        return Predict.List(response=r, list_type="voices")

    @staticmethod
    def predict(text: str, voice: str) -> "Predict.Item":
        body = {"text": text, "voice": voice}
        r = Predict.interface.send_request(rtype=RequestTypes.POST, route="", json=body)
        return Predict.Item(r)
