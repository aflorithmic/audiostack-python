from audiostack.helpers.request_interface import RequestInterface
from audiostack.helpers.request_types import RequestTypes
from audiostack.helpers.api_item import APIResponse

class TTS():
    speech_interface = RequestInterface(family="speech")
    
    class Item(APIResponse):
        
        def __init__(self, response) -> None:
            super().__init__(response)
            self.speechId = self.data["speechId"]

        def download(self, path="./", fileName="") -> None:
            
            sections = self.data["sections"]
            for i, s in enumerate(sections):
                if not fileName:
                    full_name = s["sectionName"] + ".wav"
                else:
                    full_name = f"{fileName}_{i}.wav"
                RequestInterface.download_url(s["url"], destination=path, name=full_name)
    
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
                if self.list_type == "speechIds":
                    return TTS.Item({"data" : item})

                
            except IndexError:
                self.idx = 0
                raise StopIteration  # Done iterating.
    
    
    @staticmethod
    def create(scriptId="", scriptItem=None, voice: str="") -> Item:
                
        if scriptId and scriptItem:
            raise Exception("scriptId or scriptItem should be supplied not both")
        if not (scriptId or scriptItem):
            raise Exception("scriptId or scriptItem should be supplied")
            
        if scriptItem:
            scriptId = scriptItem.scriptId
        
        body = {
            "scriptId": scriptId,
            "voice" : voice,
        }
        
        r = TTS.speech_interface.send_request(rtype=RequestTypes.POST, route="tts", json=body)
        return r, TTS.Item(r)

    @staticmethod
    def get(speechId: str) -> Item:
        
        r = TTS.speech_interface.send_request(rtype=RequestTypes.GET, route="tts", path_parameters=speechId)
        return r, TTS.Item(r)

    @staticmethod
    def list(projectName="", moduleName: str="", scriptName: str="", scriptId: str="") -> list:
        query_params = {
            "projectName" : projectName,
            "moduleName" : moduleName,
            "scriptName" : scriptName,
            "scriptId" : scriptId
        }
        r = TTS.speech_interface.send_request(rtype=RequestTypes.GET, route="tts", query_parameters=query_params)
        return r, TTS.List(r, list_type="speechIds")