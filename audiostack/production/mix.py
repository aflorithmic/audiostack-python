from audiostack.helpers.request_interface import RequestInterface
from audiostack.helpers.request_types import RequestTypes
from audiostack.helpers.api_item import APIResponse

import requests

class Mix():
    interface = RequestInterface(family="production")
    
    # class Enco(APIResponse):
    #     def __init__(self, response) -> None:
    #         super().__init__(response)
    #         self.productionId = self.data["productionId"]
    #     def download(self, fileName="", path="./") -> None:
            
    #         format = s["format"]
    #         if not fileName:
    #             full_name = f"_mix.{format}"
    #         else:
    #             full_name = f"{fileName}_{i}.{format}"
    #         RequestInterface.download_url(s["url"], destination=path, name=full_name)
    class Item(APIResponse):
        
        def __init__(self, response) -> None:
            super().__init__(response)
            self.productionId = self.data["productionId"]

        def download(self, fileName="", path="./") -> None:
            
            sections = self.data["files"]
            
            for i, s in enumerate(sections):
                format = s["format"]
                if not fileName:
                    full_name = f"default_mix.{format}"
                else:
                    full_name = f"{fileName}_{i}.{format}"
                RequestInterface.download_url(s["url"], destination=path, name=full_name)
            
        # NEEDS TO BE MOVED
        # def encode(self, preset):
        #     body = {
        #         "productionId" : self.productionId,
        #         "preset" : preset
        #     }
        #     print(body)
        #     r = requests.post(url="https://staging-v2.api.audio/delivery/encoder", json=body, headers={"x-api-key" : "" })
        #     print(r.json())
        #     return r
            
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
                if self.list_type == "productionIds":
                    return Mix.Item({"data" : item})

                
            except IndexError:
                self.idx = 0
                raise StopIteration  # Done iterating.
    
    
    @staticmethod
    def create(speechId="", speechItem=None, soundTemplate: str="") -> Item:
                
        if speechId and speechItem:
            raise Exception("speechId or scriptItem should be supplied not both")
        if not (speechId or speechItem):
            raise Exception("speechId or scriptItem should be supplied")
            
        if speechItem:
            speechId = speechItem.speechId
        
        body = {
            "speechId": speechId,
            "soundTemplate" : soundTemplate,
        }
        
        r = Mix.interface.send_request(rtype=RequestTypes.POST, route="mix", json=body)
        return r, Mix.Item(r)

    # @staticmethod
    # def get(speechId: str) -> Item:
        
    #     r = TTS.speech_interface.send_request(rtype=RequestTypes.GET, route="tts", path_parameters=speechId)
    #     return r, TTS.Item(r)

    # @staticmethod
    # def list(projectName="", moduleName: str="", scriptName: str="", scriptId: str="") -> list:
    #     query_params = {
    #         "projectName" : projectName,
    #         "moduleName" : moduleName,
    #         "scriptName" : scriptName,
    #         "scriptId" : scriptId
    #     }
    #     r = TTS.speech_interface.send_request(rtype=RequestTypes.GET, route="tts", query_parameters=query_params)
    #     return r, TTS.List(r, list_type="speechIds")