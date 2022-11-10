"""
# Content/script

converts text into a format that plays nicely with TTS
"""


from audiostack.helpers.request_interface import RequestInterface
from audiostack.helpers.request_types import RequestTypes
from audiostack.helpers.api_item import APIResponse

class Script():
    
    script_interface = RequestInterface(family="content")
        
    class Item(APIResponse):
        
        def __init__(self, response) -> None:
            super().__init__(response)
            
            self.scriptId = self.data["scriptId"]
            self.projectName = self.data["projectName"]
            self.moduletName = self.data["moduleName"]
            self.scriptName = self.data["scriptName"]
            self.scriptText = self.data["scriptText"]
                
        # def update(self):
        #     Script.update(self.response)
        #     pass
        def delete(self):
            return Script.delete(self.scriptId)
        
            
        
        # def __str__(self) -> str:
        #      return "hello"
    
    class List(APIResponse):
        def __init__(self, response, list_type) -> None:
            super().__init__(response)

            self.items = self.response["data"][list_type]
            self.idx = 0
            self.list_type = list_type
            
        # todo move this to base class
        def __iter__(self):
            return self
        
        def __next__(self):
            
            self.idx += 1
            try:
                item = self.items[self.idx-1]
                if self.list_type == "scripts":
                    return Script.Item({"data" : item})

                
            except IndexError:
                self.idx = 0
                raise StopIteration  # Done iterating.

        
    @staticmethod
    def create(scriptText: str, projectName: str="", moduleName: str="", scriptName: str="", metadata: dict={}) -> Item:
        
        body = {
            "scriptText" : scriptText,
            "projectName" : projectName,
            "moduleName" : moduleName,
            "scriptName" : scriptName,
            "metadata" : metadata
        }
        
        r = Script.script_interface.send_request(rtype=RequestTypes.POST, route="script", json=body)
        return r, Script.Item(r)
    
    @staticmethod
    def get(scriptId: str, version: str="") -> Item:
        
        path_params = f"{scriptId}/{version}" if version else scriptId
        r = Script.script_interface.send_request(rtype=RequestTypes.GET, route="script", path_parameters=path_params)
        return r, Script.Item(r)
        
    @staticmethod
    def delete(scriptId: str, version: str=""):
        
        path_params = f"{scriptId}/{version}" if version else scriptId
        r = Script.script_interface.send_request(rtype=RequestTypes.DELETE, route="script", path_parameters=path_params)
        return r
        
    
    # def update(self):
    #     pass
    
    
    @staticmethod
    def list(projectName="", moduleName: str="", scriptName: str="", scriptId: str="") -> list:
        query_params = {
            "projectName" : projectName,
            "moduleName" : moduleName,
            "scriptName" : scriptName,
            "scriptId" : scriptId
        }
        r = Script.script_interface.send_request(rtype=RequestTypes.GET, route="scripts", query_parameters=query_params)
        return r, Script.List(r, list_type="scripts")

    

        
    
