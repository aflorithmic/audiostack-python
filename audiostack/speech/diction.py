from typing import Any, Union

from audiostack.helpers.api_item import APIResponseItem
from audiostack.helpers.api_list import APIResponseList
from audiostack.helpers.request_interface import RequestInterface
from audiostack.helpers.request_types import RequestTypes


class Diction:
    interface = RequestInterface(family="speech/diction")

    class Item(APIResponseItem):
        def __init__(self, response: dict) -> None:
            super().__init__(response)
            self.lang = self.data["lang"]
            self.words = self.data["words"]
            self.wordCategory = self.data.get("wordCategory", "")
            self.content = self.data.get("content", "")

    class Word(APIResponseItem):
        def __init__(self, response: dict) -> None:
            super().__init__(response)
            self.inputs = self.data["inputs"]
            self.replacements = self.data["replacements"]

    class List(APIResponseList):
        def __init__(self, response: dict, list_type: str) -> None:
            super().__init__(response, list_type)

        def resolve_item(
            self, list_type: str, item: Any
        ) -> Union["Diction.Item", "Diction.Word"]:
            if list_type == "dictionaries":
                return Diction.Item({"data": item})
            elif list_type == "words":
                return Diction.Word({"data": item})
            else:
                raise Exception()

    @staticmethod
    def list() -> "Diction.List":
        r = Diction.interface.send_request(rtype=RequestTypes.GET, route="")
        return Diction.List(r, "dictionaries")

    class Custom:
        @staticmethod
        def list() -> "Diction.List":
            r = Diction.interface.send_request(rtype=RequestTypes.GET, route="custom")
            return Diction.List(r, "dictionaries")

        @staticmethod
        def create_word(
            word: str,
            replacement: str,
            lang: str = "global",
            specialization: str = "default",
            contentType: str = "basic",
        ) -> "Diction.Word":
            body = {
                "word": word,
                "replacement": replacement,
                "lang": lang,
                "specialization": specialization,
                "contentType": contentType,
            }

            r = Diction.interface.send_request(
                rtype=RequestTypes.PUT, route="custom/item", json=body
            )
            return Diction.Word(r)

        @staticmethod
        def list_words(lang: str) -> "Diction.List":
            r = Diction.interface.send_request(
                rtype=RequestTypes.GET,
                route="custom/items",
                query_parameters={"lang": lang},
            )
            return Diction.List(r, "words")

        @staticmethod
        def delete_word(
            lang: str, word: str, specialization: str = ""
        ) -> APIResponseItem:
            query = {"lang": lang, "word": word, "specialization": specialization}
            r = Diction.interface.send_request(
                rtype=RequestTypes.DELETE, route="custom/item", query_parameters=query
            )
            return APIResponseItem(r)
