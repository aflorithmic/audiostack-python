from audiostack.helpers.request_interface import RequestInterface
from audiostack.helpers.request_types import RequestTypes
from audiostack.helpers.api_item import APIResponseItem
from audiostack.helpers.api_list import APIResponseList


class Voice:
    interface = RequestInterface(family="speech/voice")

    class Item(APIResponseItem):
        def __init__(self, response) -> None:
            super().__init__(response)
            self.provider = self.data["provider"]
            self.alias = self.data["alias"]

    class List(APIResponseList):
        def __init__(self, response, list_type) -> None:
            super().__init__(response, list_type)

        def resolve_item(self, list_type, item):
            if list_type == "voices":
                return Voice.Item({"data": item})
            else:
                raise Exception()

    @staticmethod
    def select_for_script(
        scriptId: str = "", scriptItem="", tone: str = "", targetLength: int = 20
    ):
        if scriptId and scriptItem:
            raise Exception("scriptId or scriptItem should be supplied not both")
        if not (scriptId or scriptItem):
            raise Exception("scriptId or scriptItem should be supplied")

        if scriptItem:
            scriptId = scriptItem.scriptId

        body = {"scriptId": scriptId, "tone": tone, "targetLength": targetLength}

        r = Voice.interface.send_request(
            rtype=RequestTypes.POST, route="select", json=body
        )
        return APIResponseItem(r)

    @staticmethod
    def select_for_content(content, tone: str = ""):
        body = {"content": content}
        if tone:
            body["tone"] = tone

        r = Voice.interface.send_request(
            rtype=RequestTypes.POST, route="select", json=body
        )
        return APIResponseItem(r)

    @staticmethod
    def list() -> list:
        r = Voice.interface.send_request(rtype=RequestTypes.GET, route="")
        return Voice.List(r, list_type="voices")

    class Parameter:
        @staticmethod
        def get() -> dict:
            r = Voice.interface.send_request(rtype=RequestTypes.GET, route="parameter")
            return APIResponseItem(r)
