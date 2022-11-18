from audiostack.helpers.request_interface import RequestInterface
from audiostack.helpers.request_types import RequestTypes
from audiostack.helpers.api_item import APIResponseItem
from audiostack.helpers.api_list import APIResponseList

class Documentation():
    
    interface = RequestInterface(family="")
        
    # class Item(APIResponseItem):
        
    #     def __init__(self, response) -> None:
    #         super().__init__(response)
            
    #         self.scriptId = self.data["scriptId"]
    #         self.projectName = self.data["projectName"]
    #         self.moduletName = self.data["moduleName"]
    #         self.scriptName = self.data["scriptName"]
    #         self.scriptText = self.data["scriptText"]
                
    #     def update(self, scriptText):
    #         return Script.update(scriptId=self.scriptId, scriptText=scriptText)
    #     def delete(self):
    #         return Script.delete(self.scriptId)
        
            
    #     def __str__(self) -> str:
    #          return self.response
    
    # class List(APIResponseList):
    #     def __init__(self, response, list_type) -> None:
    #         super().__init__(response, list_type)

    #     def resolve_item(self, list_type, item):
    #         if list_type == "scripts":
    #             return Script.Item({"data" : item})
    #         else:
    #             raise Exception()


    
    @staticmethod
    def docs_for_service(service: object) -> dict:
        service = service.__name__.lower()

        r = Documentation.interface.send_request(rtype=RequestTypes.GET, route="documentation", query_parameters={"route" : service})
        return r
        

