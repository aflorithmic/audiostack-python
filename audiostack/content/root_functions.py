
from audiostack.helpers.request_interface import RequestInterface
from audiostack.helpers.request_types import RequestTypes
from audiostack.helpers.api_item import APIResponse

class Root: 
    interface = RequestInterface(family="content")

    def list_projects() -> list:
        r = Root.interface.send_request(rtype=RequestTypes.GET, route="list_projects")
        return r, r.json()["data"]