from audiostack.helpers.request_interface import RequestInterface
from audiostack.helpers.request_types import RequestTypes
from audiostack.helpers.api_item import APIResponseItem



class Encoder():
    interface = RequestInterface(family="delivery")
    
    class Item(APIResponseItem):
        
        def __init__(self, response) -> None:
            super().__init__(response)
            self.url = self.data["url"]
            self.format = self.data["format"]

        def download(self, fileName="default", path="./") -> None:
            
            full_name = f"{fileName}.{self.format}"
            RequestInterface.download_url(self.url, destination=path, name=full_name)
            
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
                
    @staticmethod
    def encode_mix(productionId: str="", productionItem: object=None, prest: str="") -> Item:
                
        if productionId and productionItem:
            raise Exception("productionId or productionItem should be supplied not both")
        if not (productionId or productionItem):
            raise Exception("productionId or productionItem should be supplied")
            
        if productionItem:
            productionId = productionItem.productionId
        
        body = {
            "productionId": productionId,
            "preset": prest
        }
        
        r = Encoder.interface.send_request(rtype=RequestTypes.POST, route="encoder", json=body)
        print(r)
        return r, Encoder.Item(r)

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