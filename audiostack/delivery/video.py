from audiostack.helpers.request_interface import RequestInterface
from audiostack.helpers.request_types import RequestTypes
from audiostack.helpers.api_item import APIResponseItem

class Video:
    interface = RequestInterface(family="delivery")

    class Item(APIResponseItem):
        def __init__(self, response) -> None:
            super().__init__(response)
            self.url = self.data["url"]
            self.format = self.data["format"]

        def download(self, fileName="default", path="./") -> None:
            full_name = f"{fileName}.{self.format}"
            RequestInterface.download_url(self.url, destination=path, name=full_name)

    @staticmethod
    def create(
        productionId: str = "",
        productionItem: object = None,
        public: bool = False,
    ) -> Item:
        
        if productionId and productionItem:
            raise Exception(
                "productionId or productionItem should be supplied not both"
            )
        if not (productionId or productionItem):
            raise Exception("productionId or productionItem should be supplied")

        if productionItem:
            try:
                productionId = productionItem.productionId
            except Exception:
                raise Exception(
                    "supplied productionItem is missing an attribute, productionItem should be type object and a response from Production.Mix"
                )
        elif productionId:
            if not isinstance(productionId, str):
                raise Exception("supplied productionId should be a uuid string.")
        

        body = {
            "productionId": productionId,
            "public": public,
        }
        r = Video.interface.send_request(
            rtype=RequestTypes.POST, route="video", json=body
        )
        
        while r["statusCode"] == 202:
            videoId = r["data"]["videoId"]
            r = Video.interface.send_request(
                rtype=RequestTypes.GET, route="video", path_parameters=videoId
            )
        return Video.Item(r)