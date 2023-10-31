from audiostack.helpers.request_interface import RequestInterface
from audiostack.helpers.request_types import RequestTypes
from audiostack.helpers.api_item import APIResponseItem
from audiostack.helpers.api_list import APIResponseList

from typing import Union


class Sound:
    interface = RequestInterface(family="production/sound")

    # ----------------------------------------- TEMPLATE -----------------------------------------
    class Template:
        class Item(APIResponseItem):
            def __init__(self, response) -> None:
                super().__init__(response)

                if "template" in self.data:  #
                    self.data = self.data["template"]

        class List(APIResponseList):
            def __init__(self, response, list_type) -> None:
                super().__init__(response, list_type)

            def resolve_item(self, list_type, item):
                if list_type == "templates":
                    return Sound.Template.Item(
                        {"data": item, "statusCode": self.response["statusCode"]}
                    )
                else:
                    raise Exception()

        @staticmethod
        def select_for_script(
            scriptId="", scriptItem="", mood: str = ""
        ) -> APIResponseItem:
            if scriptId and scriptItem:
                raise Exception("scriptId or scriptItem should be supplied not both")
            if not (scriptId or scriptItem):
                raise Exception("scriptId or scriptItem should be supplied")

            if scriptItem:
                scriptId = scriptItem.scriptId

            body = {"scriptId": scriptId, "mood": mood}

            r = Sound.interface.send_request(
                rtype=RequestTypes.POST, route="select", json=body
            )
            return APIResponseItem(response=r)

        @staticmethod
        def select_for_content(content: str, mood: str = "") -> APIResponseItem:
            body = {"content": content}
            if mood:
                body["mood"] = mood

            r = Sound.interface.send_request(
                rtype=RequestTypes.POST, route="select", json=body
            )
            return APIResponseItem(response=r)

        @staticmethod
        def list(
            collections: Union[str, list] = "",
            genres: Union[str, list] = "",
            instruments: Union[str, list] = "",
            moods: str = "",
        ) -> list:
            query_params = {
                "moods": moods,
                "collections": collections,
                "instruments": instruments,
                "genres": genres,
            }
            r = Sound.interface.send_request(
                rtype=RequestTypes.GET, route="template", query_parameters=query_params
            )
            return Sound.Template.List(r, list_type="templates")

        def create(templateName: str, description: str = ""):
            body = {"templateName": templateName, "description": description}
            r = Sound.interface.send_request(
                rtype=RequestTypes.POST, route="template", json=body
            )
            return Sound.Template.Item(r)

        def delete(templateName: str):
            r = Sound.interface.send_request(
                rtype=RequestTypes.DELETE,
                route="template",
                path_parameters=templateName,
            )
            return APIResponseItem(r)

    # ----------------------------------------- TEMPLATE SEGMENT -----------------------------------------
    class Segment:
        def create(mediaId: str, templateName: str, soundSegmentName: str):
            segment = {
                "templateName": templateName,
                "segmentName": soundSegmentName,
                "mediaId": mediaId,
            }
            r = Sound.interface.send_request(
                rtype=RequestTypes.POST, route="segment", json=segment
            )
            return Sound.Template.Item(r)

    # ----------------------------------------- TEMPLATE PARAMETERS -----------------------------------------
    class Parameter:
        @staticmethod
        def get() -> dict:
            r = Sound.interface.send_request(rtype=RequestTypes.GET, route="parameter")
            return APIResponseItem(r)
