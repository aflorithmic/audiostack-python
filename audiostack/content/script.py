"""
# Content/script

converts text into a format that plays nicely with TTS
"""


from audiostack.helpers.request_interface import RequestInterface
from audiostack.helpers.request_types import RequestTypes
from audiostack.helpers.api_item import APIItem

class Script():
    
    script_interface = RequestInterface(family="content")
        
    class Item(APIItem):
        
        def __init__(self, response) -> None:
            super().__init__(response)
            
            self.scriptId = self.response["data"]["scriptId"]
        
        def update(self):
            Script.update(self.response)
            pass
        def delete():
            pass
        
        def __str__(self) -> str:
             return "hello"
    
        
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
    
    def get() -> Item:
        return 
        
    
    def delete(self):
        pass
    
    def update(self):
        pass
    
    
    @staticmethod
    def list() -> list:
        pass
    
    
