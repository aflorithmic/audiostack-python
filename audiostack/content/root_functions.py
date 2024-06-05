from audiostack.helpers.api_item import APIResponseItem
from audiostack.helpers.request_interface import RequestInterface
from audiostack.helpers.request_types import RequestTypes


class Root:
    interface = RequestInterface(family="content")

    @staticmethod
    def list_projects() -> APIResponseItem:
        r = Root.interface.send_request(rtype=RequestTypes.GET, route="list_projects")
        return APIResponseItem(r)

    @staticmethod
    def list_modules(projectName: str) -> APIResponseItem:
        r = Root.interface.send_request(
            rtype=RequestTypes.GET,
            route="list_projects",
            query_parameters={"projectName": projectName},
        )
        return APIResponseItem(r)

    @staticmethod
    def generate(prompt: str, max_length: int = 100) -> APIResponseItem:
        r = Root.interface.send_request(
            rtype=RequestTypes.POST,
            route="generate",
            json={"prompt": prompt, "max_length": max_length},
        )
        return APIResponseItem(r)
