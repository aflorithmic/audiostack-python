from audiostack.helpers.request_interface import RequestInterface
from audiostack.helpers.request_types import RequestTypes
from audiostack.helpers.api_item import APIResponseItem
from audiostack.helpers.api_list import APIResponseList


class Predict:
    interface = RequestInterface(family="speech/predict")

    class Item(APIResponseItem):
        def __init__(self, response) -> None:
            super().__init__(response)

            self.length = self.data["length"]

    class List(APIResponseList):
        def __init__(self, response, list_type) -> None:
            super().__init__(response, list_type)

        def resolve_item(self, list_type, item):
            if list_type == "voices":
                return item
            else:
                raise Exception()

    @staticmethod
    def list() -> list:
        r = Predict.interface.send_request(rtype=RequestTypes.GET, route="voices")
    #    return #Predict.List(r, list_type="voices")
        return Predict.List(response=r, list_type="voices")
    

    @staticmethod
    def predict(text: str, voice: str) -> list:
        body = {
            "text" : text,
            "voice" : voice
        }
        r = Predict.interface.send_request(rtype=RequestTypes.POST, route="", json=body)
        return Predict.Item(r)