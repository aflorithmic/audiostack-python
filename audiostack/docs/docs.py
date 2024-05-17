from audiostack.helpers.api_item import APIResponseItem
from audiostack.helpers.request_interface import RequestInterface
from audiostack.helpers.request_types import RequestTypes


class Documentation:
    interface = RequestInterface(family="")

    @staticmethod
    def docs_for_service(service: object) -> APIResponseItem:
        service = service.__name__.lower()  # type: ignore

        r = Documentation.interface.send_request(
            rtype=RequestTypes.GET,
            route="documentation",
            query_parameters={"route": service},
        )
        return APIResponseItem(r)
