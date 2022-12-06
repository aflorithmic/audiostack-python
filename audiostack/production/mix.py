from audiostack.helpers.request_interface import RequestInterface
from audiostack.helpers.request_types import RequestTypes
from audiostack.helpers.api_item import APIResponseItem
from audiostack.helpers.api_list import APIResponseList

class Mix():
    interface = RequestInterface(family="production")
    
    class Item(APIResponseItem):
        
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
                    full_name = f"{fileName}.{format}"
                RequestInterface.download_url(s["url"], destination=path, name=full_name)
                
        def delete(self):
            return Mix.delete(self.productionId)
 
    class List(APIResponseList):
        def __init__(self, response, list_type) -> None:
            super().__init__(response, list_type)

        def resolve_item(self, list_type, item):
            if list_type == "productionIds":
                return Mix.Item({"data" : item})
            else:
                raise Exception()

    @staticmethod
    def create(
        speechId="", 
        speechItem=None, 
        soundTemplate: str="",
        forceLength: float=0.0, # a value of 0 means no force length
        mediaFiles: dict={},
        sectionProperties: dict={},
        masteringPreset: str="",
        acousticSpace: str="",
        callbackUrl: str=""
        ) -> Item:
                
        if speechId and speechItem:
            raise Exception("speechId or scriptItem should be supplied not both")
        if not (speechId or speechItem):
            raise Exception("speechId or scriptItem should be supplied")
        
        try:
            isinstance(speechItem.soundTemplate, str)
        except:
            raise Exception("soundTemplate argument should be a string")

            
        if speechItem:
            speechId = speechItem.speechId
        
        body = {
            "speechId": speechId,
            "soundTemplate" : soundTemplate,
            "forceLength": forceLength, 
            "mediaFiles": mediaFiles, 
            "sectionProperties": sectionProperties,
            "masteringPreset": masteringPreset,
            "acousticSpace": acousticSpace,
            "callbackUrl": callbackUrl
        }
        
        r = Mix.interface.send_request(rtype=RequestTypes.POST, route="mix", json=body)
        return Mix.Item(r)

    @staticmethod
    def get(productionId: str) -> Item:
        
        r = Mix.interface.send_request(rtype=RequestTypes.GET, route="mix", path_parameters=productionId)
        return Mix.Item(r)

    @staticmethod
    def delete(productionId: str) -> str:
        r = Mix.interface.send_request(rtype=RequestTypes.DELETE, route="mix", path_parameters=productionId)
        return r

    @staticmethod
    def list(projectName="", moduleName: str="", scriptName: str="", scriptId: str="") -> list:
        query_params = {
            "projectName" : projectName,
            "moduleName" : moduleName,
            "scriptName" : scriptName,
            "scriptId" : scriptId
        }
        r = Mix.interface.send_request(rtype=RequestTypes.GET, route="mixes", query_parameters=query_params)
        print(r)
        return Mix.List(r, list_type="productionIds")
    