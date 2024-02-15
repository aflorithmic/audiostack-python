from typing import List

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

    @staticmethod
    def create(text: str, category: str, tags: List, number_of_results: int = 1) -> Item:
        payload = {
            "text": text,
            "category": category,
            "tags": tags,
            "number_of_results": number_of_results
        }
        r = RecommendTag.interface.send_request(
            rtype=RequestTypes.POST,
            route="recommend/tag",
            json=payload,
        )
        return RecommendTag.Item(r)
    
class RecommendMood:
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
            if list_type == "RecommendMoods":
                return RecommendMood.Item({"data": item})
            else:
                raise Exception()

    @staticmethod
    def create(text: str, number_of_results: int = 1) -> Item:
        payload = {
            "text": text,
            "number_of_results": number_of_results
        }
        r = RecommendMood.interface.send_request(
            rtype=RequestTypes.POST,
            route="recommend/mood",
            json=payload,
        )
        return RecommendMood.Item(r)
    
class RecommendTone:
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
            if list_type == "RecommendTones":
                return RecommendTone.Item({"data": item})
            else:
                raise Exception()

    @staticmethod
    def create(text: str, number_of_results: int = 1) -> Item:
        payload = {
            "text": text,
            "number_of_results": number_of_results
        }
        r = RecommendTone.interface.send_request(
            rtype=RequestTypes.POST,
            route="recommend/tone",
            json=payload,
        )
        return RecommendTone.Item(r)