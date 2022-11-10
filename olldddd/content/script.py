"""
# Content/script

converts text into a format that plays nicely with TTS
"""
import requests
class API():
    
    api_key = "0b1173a6420c4c028690b7beff39c0ad"
    api_base = "https://staging-v2.api.audio"
    
    def __remove_empty(d):
        final_dict = {}
        for a, b in d.items():
            if b:
            if isinstance(b, dict):
                final_dict[a] = remove_empty(b)
            elif isinstance(b, list):
                final_dict[a] = list(filter(None, [remove_empty(i) for i in b]))
            else:
                final_dict[a] = b
        return final_dict
    
    
    def __header():
        return {'x-api-key' : API.api_key}
    
    def _post(path, json):
        
        return requests.post(
            url=f"{API.api_base}/{path}", 
            json=API.__remove_empty(json), 
            headers=API.__header()
        )
        
    def _put():
        pass
    def _patch():
        pass
    
    def _get():
        pass
    def _delete():
        pass

class Interface():
    
    def __init__(self, family, base_url, service_name ) -> None:
        self.family = family
        self.base_url = base_url
        self.service_name = service_name
    
    def create(self, body={}):
        #return API._post(path=f"{self.family}/{self.base_url}", json=body)
        return API._post(path=f"{self.base_url}", json=body)
    
    def update():
        return API._put()
    
    def delete():
        return API._delete()
    
    def list():
        return API._list()
    
    
class Script():
    
    interface = Interface(family="content", base_url="script", service_name="script")
    
    class Item():
        
        def __init__(self, body) -> None:
            self.body = body
        
        def update(self):
            Script.update(self.body)
            pass
        def delete():
            pass           
    
    @staticmethod
    def create(scriptText: str, projectName: str="", moduleName: str="", scriptName: str="", metadata: dict={}) -> Item:
        r = Script.interface.create(
            body={
                "scriptText" : scriptText,
                "projectName" : projectName,
                "moduleName" : moduleName,
                "scriptName" : scriptName,
                "metadata" : metadata
                }
            )
        return r
        return Script.Item({"name" : "sam"})
    
    def get() -> Item:
        return 
        
    
    def delete(self):
        pass
    
    def update(self):
        pass
    
    
    @staticmethod
    def list() -> list:
        pass
        