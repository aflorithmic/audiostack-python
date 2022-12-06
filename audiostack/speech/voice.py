from audiostack.helpers.request_interface import RequestInterface
from audiostack.helpers.request_types import RequestTypes
from audiostack.helpers.api_item import APIResponseItem
from audiostack.helpers.api_list import APIResponseList

class Voice():
    interface = RequestInterface(family="speech/voice")
    
    OBJECT_NAME = "voice"
    resource_path = "/voice"
    list_parameters_path = "/voice/parameter"

    @staticmethod
    def get() -> dict:
        r = Voice.interface.send_request(rtype=RequestTypes.GET, route="parameter")
        return r


   