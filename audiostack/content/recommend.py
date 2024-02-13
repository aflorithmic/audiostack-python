from audiostack.helpers.request_interface import RequestInterface
from audiostack.helpers.request_types import RequestTypes
from audiostack.helpers.api_item import APIResponseItem
from audiostack.helpers.api_list import APIResponseList

class RecommendTag:
    FAMILY = "content"
    interface = RequestInterface(family=FAMILY)

    class Item(APIResponseItem):
        def __init__(self, response) -> None:
            super().__init__(response)

            self.category = self.data["category"]
            self.tag = self.data["tag"]

    class List(APIResponseList):
        def __init__(self, response, list_type) -> None:
            super().__init__(response, list_type)

        def resolve_item(self, list_type, item):
            if list_type == "RecommendTags":
                return RecommendTag.Item({"data": item})
            else:
                raise Exception()

    @staticmethod
    def post(text: str, category: str, tags: List[str], number_of_results: int = 1) -> Item:
        path_parameters = ""
        query_parameters = {
            "text": text,
            "category": category,
            "tags": tags,
            "number_of_results": number_of_results
        }
        r = RecommendTag.interface.send_request(
            rtype=RequestTypes.GET,
            route="recommend/tag",
            path_parameters=path_parameters,
            query_parameters=query_parameters,
        )
        return RecommendTag.Item(r)