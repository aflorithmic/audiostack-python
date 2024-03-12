from audiostack.helpers.request_interface import RequestInterface
from audiostack.helpers.request_types import RequestTypes
from audiostack.helpers.api_item import APIResponseItem
from audiostack.helpers.api_list import APIResponseList
import os


class File:
    FAMILY = "content"
    interface = RequestInterface(family=FAMILY)

    class Item(APIResponseItem):
        def __init__(self, response) -> None:
            super().__init__(response)
            self.fileId = self.data["fileId"]
            self.filePath = self.data["filePath"]
            self.url = self.data.get("url", None)

        def delete(self):
            return File.delete(self.fileId)
    
        def download(self, fileName="", path="./") -> None:
            if not fileName:
                fileName = self.filePath.split("/")[-1]
            RequestInterface.download_url(self.url, destination=path, name=fileName)

    class List(APIResponseList):
        def __init__(self, response, list_type) -> None:
            super().__init__(response, list_type)

        def resolve_item(self, list_type, item):
            if list_type == "items" or list_type == "files":
                return File.Item({"data": item})
            else:
                raise Exception()

    @staticmethod
    def create(
        localPath: str,
        uploadPath: str,
        fileType: str,
        category: str = "",
        tags: list = [],
        metadata: dict = {},
        filePath: str = None,
    ) -> Item:
        if not os.path.isfile(localPath):
            raise Exception("Supplied file does not eixst")

        if not uploadPath or not localPath:
            raise Exception(
                "Please supply a localPath (path to your local file) and an uploadPath (path to where youd like this to be saved)"
            )

        data = {
            "filePath": uploadPath,
            "fileType": fileType,
            "source": "pythonSDK",
            "category": category,
            "tags": tags,
            "metadata": metadata,
        }

        r = File.interface.send_request(
            rtype=RequestTypes.POST,
            route="file/create-upload-url",
            json=data,
        )
        response = APIResponseItem(r)
        url = response.data["fileUploadUrl"]
        fileId = response.data["fileId"]

        status = File.interface.send_upload_request(
            local_path=localPath, upload_url=url
        )
        return File.get(fileId)

    @staticmethod
    def transfer(
        url: str,
        uploadPath: str,
        category: str = "",
        tags: list = [],
        metadata: dict = {},
    ) -> Item:

        data = {
            "filePath": uploadPath,
            "url": url,
            "category": category,
            "tags": tags,
            "metadata": metadata,
        }

        r = File.interface.send_request(
            rtype=RequestTypes.PUT,
            route="file/transfer-file",
            json=data,
        )
        response = APIResponseItem(r)
        return File.get(response.data["fileId"])

    @staticmethod
    def modify(
        fileId: str,
        filePath: str = "",
        category: str = "",
        tags: list = [],
        metadata: dict = {},
    ) -> Item:

        data = {
            "filePath": filePath,
            "category": category,
            "tags": tags,
            "metadata": metadata,
        }

        r = File.interface.send_request(
            rtype=RequestTypes.PATCH,
            route=f"file/id/{fileId}",
            json=data,
        )
        return File.get(fileId)

    @staticmethod
    def get(fileId: str) -> Item:
        r = File.interface.send_request(
            rtype=RequestTypes.GET, route="file/id", path_parameters=fileId
        )
        return File.Item(r)

    @staticmethod
    def delete(fileId: str) -> str:
        r = File.interface.send_request(
            rtype=RequestTypes.DELETE, route="file/id", path_parameters=fileId
        )
        return APIResponseItem(r)

    @staticmethod
    def search(
        path: str = "",
        source: str = "",
        tags: list = [],
        name: str = "",
        fileType: str = "",
        category: str = "",
        sortBy: str = "",
    ) -> List:
        queries = {
            "path": path,
            "source": source,
            "tags": tags,
            "name": name,
            "fileType": fileType,
            "category": category,
            "soryBy": sortBy,
        }
        r = File.interface.send_request(
            rtype=RequestTypes.GET, route="file/search", query_parameters=queries
        )
        return File.List(r, list_type="items")


class Folder:
    FAMILY = "content"
    interface = RequestInterface(family=FAMILY)

    class Item(APIResponseItem):
        def __init__(self, response) -> None:
            super().__init__(response)
            self.folders = Folder.List(response, list_type="folders")
            self.files = File.List(response, list_type="files")

    class List(APIResponseList):
        def __init__(self, response, list_type) -> None:
            super().__init__(response, list_type)

        def resolve_item(self, list_type, item):
            if list_type == "folders":
                return {"data": item}
            else:
                raise Exception()

    @staticmethod
    def create(name) -> Item:

        r = File.interface.send_request(
            rtype=RequestTypes.POST,
            route="folder",
            json={"folder": name},
        )
        return APIResponseItem(r)

    @staticmethod
    def list(folder: str) -> Item:
        r = File.interface.send_request(
            rtype=RequestTypes.GET, route="folder", query_parameters={"folder": folder}
        )
        return Folder.Item(r)

    @staticmethod
    def delete(folder: str, delete_files=False) -> str:
        r = File.interface.send_request(
            rtype=RequestTypes.DELETE,
            route="folder",
            query_parameters={"folder": folder, "forceDelete": delete_files},
        )
        return APIResponseItem(r)
