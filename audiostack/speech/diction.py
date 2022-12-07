from audiostack.helpers.request_interface import RequestInterface
from audiostack.helpers.request_types import RequestTypes
from audiostack.helpers.api_item import APIResponseItem
from audiostack.helpers.api_list import APIResponseList

class Diction():
    interface = RequestInterface(family="speech/diction")
    
    # class Item(APIResponseItem):
        
    #     def __init__(self, response) -> None:
    #         super().__init__(response)
    #         self.provider = self.data["provider"]
    #         self.alias = self.data["alias"]

    # class List(APIResponseList):
    #     def __init__(self, response, list_type) -> None:
    #         super().__init__(response, list_type)

    #     def resolve_item(self, list_type, item):
    #         if list_type == "voices":
    #             return Voice.Item({"data" : item})
    #         else:
    #             raise Exception()

    
    @staticmethod
    def list() -> list:
        r = Diction.interface.send_request(rtype=RequestTypes.GET, route="")
        return APIResponseItem(r)

    # class Parameter():
        
    #     @staticmethod
    #     def get() -> dict:
    #         r = Voice.interface.send_request(rtype=RequestTypes.GET, route="parameter")
    #         return r

   