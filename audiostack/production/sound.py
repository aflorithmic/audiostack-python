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

                self.templateName = self.data["alias"]
                self.tags = self.data["tags"]
                self.samples = self.data["samples"]

        class List(APIResponseList):
            def __init__(self, response, list_type) -> None:
                super().__init__(response, list_type)

            def resolve_item(self, list_type, item):
                if list_type == "templates":
                    return Sound.Template.Item({"data": item})
                else:
                    raise Exception()

        @staticmethod
        def list(
            collections: Union[str, list] = "",
            genres: Union[str, list] = "",
            instruments: Union[str, list] = "",
            moods: str = "",
            # tempo: str = "",  # TO BE DONE its missing in TAG_DATA get_parameters.py in ms-sound-templates-v3
        ) -> list:

            query_params = {
                "moods": moods,
                "collections": collections,
                "insturments": instruments,
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

        # def update(
        #     templateName: str,
        #     description: str = "",
        #     genre: str = "",
        #     collections: list = None,
        #     tags: list = None,
        # ):
        #     body = {
        #         "templateName": templateName,
        #         "description": description,
        #         "genre": genre,
        #         "collections": collections,
        #         "tags": tags,
        #     }
        #     r = Sound.interface.send_request(
        #         rtype=RequestTypes.PUT, route="template", json=body
        #     )
        #     return Sound.Template.Item(r)

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
