from audiostack.helpers.request_interface import RequestInterface
from audiostack.helpers.request_types import RequestTypes
from audiostack.helpers.api_item import APIResponseItem
from audiostack.helpers.api_list import APIResponseList


class Documentation:
    interface = RequestInterface(family="")

    @staticmethod
    def docs_for_service(service: object) -> dict:
        service = service.__name__.lower()

        r = Documentation.interface.send_request(
            rtype=RequestTypes.GET,
            route="documentation",
            query_parameters={"route": service},
        )
        return APIResponseItem(r)
