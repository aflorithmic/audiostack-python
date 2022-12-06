from audiostack.helpers.request_interface import RequestInterface
from audiostack.helpers.request_types import RequestTypes
from audiostack.helpers.api_item import APIResponseItem
from audiostack.helpers.api_list import APIResponseList

class Voice():
    interface = RequestInterface(family="speech")
    
    OBJECT_NAME = "voice"
    resource_path = "/voice"
    list_parameters_path = "/voice/parameter"

    @classmethod
    def list_parameters(cls):
        return cls._get_request(path_param=cls.list_parameters_path)


   