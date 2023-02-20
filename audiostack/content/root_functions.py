from audiostack.helpers.request_interface import RequestInterface
from audiostack.helpers.request_types import RequestTypes
from audiostack.helpers.api_item import APIResponseItem


class Root:
    interface = RequestInterface(family="content")

    def list_projects() -> list:
        r = Root.interface.send_request(rtype=RequestTypes.GET, route="list_projects")
        return APIResponseItem(r)

    def list_modules(projectName: str) -> list:
        r = Root.interface.send_request(
            rtype=RequestTypes.GET,
            route="list_projects",
            query_parameters={"projectName": projectName},
        )
        return APIResponseItem(r)
