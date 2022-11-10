from audiostack.helpers.request_interface import RequestInterface
from audiostack.helpers.request_types import RequestTypes

class TTS():
    speech_interface = RequestInterface(family="speech")
    
    class Item():
        
        def __init__(self, body) -> None:
            self.body = body
            self.speechId = self.body["data"]["speechId"]

        def download(self, path="./", fileName="") -> None:
            
            sections = self.body["data"]["sections"]
            for i, s in enumerate(sections):
                if not fileName:
                    full_name = s["sectionName"] + ".wav"
                else:
                    full_name = f"{fileName}_{i}.wav"
                RequestInterface.download_url(s["url"], destination=path, name=full_name)
    
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
