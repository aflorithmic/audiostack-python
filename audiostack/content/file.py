import os
import time
from typing import Any, Optional
from uuid import UUID

from audiostack import TIMEOUT_THRESHOLD_S
from audiostack.helpers.api_item import APIResponseItem
from audiostack.helpers.api_list import APIResponseList
from audiostack.helpers.request_interface import RequestInterface
from audiostack.helpers.request_types import RequestTypes


class File:
    FAMILY = "content"
    interface = RequestInterface(family=FAMILY)

    class Item(APIResponseItem):
        def __init__(self, response: dict) -> None:
            super().__init__(response)
            self.file_id = response["fileId"]
            self.file_name = response["fileName"]
            self.url = response.get("url", None)
            self.created_by = response["createdBy"]
            self.last_modified = response.get("lastModified", None)
            self.file_type_id = response["fileTypeId"]
            self.category_id = response.get("categoryId", None)
            self.size = response["size"]
            self.created_at = response["createdAt"]
            self.status = response["status"]

        def download(self, fileName: str, path: str = "./") -> None:
            if not fileName:
                raise Exception("Please supply a valid file name")
            if not self.url:
                raise Exception("No URL found for this file")
            RequestInterface.download_url(self.url, destination=path, name=fileName)

    class List(APIResponseList):
        def __init__(self, response: dict, list_type: str) -> None:
            super().__init__(response, list_type)

        def resolve_item(self, list_type: str, item: Any) -> "File.Item":
            if list_type == "items" or list_type == "files":
                return File.Item({"data": item})
            else:
                raise Exception()

    @staticmethod
    def create(
        local_path: str,
        file_name: str,
        folder_id: Optional[UUID] = None,
        category: str = "",
    ) -> Item:
        if not local_path:
            raise Exception("Please supply a localPath (path to your local file)")

        if not os.path.isfile(local_path):
            raise Exception("Supplied file does not eixst")

        if not file_name:
            raise Exception("Please supply a valid file name")

        if not folder_id:
            Folder.get_root().data["folders"]["folderId"]

        category_id = File.get_category_id_by_name(category)

        payload = {
            "fileName": file_name,
            "folderId": folder_id,
            "categoryId": category_id,
        }

        r = File.interface.send_request(
            rtype=RequestTypes.POST,
            route="file/create-upload-url",
            json=payload,
            overwrite_base_url="https://v2.api.audio/v3",
        )
        response = APIResponseItem(r)
        url = response.data["uploadUrl"]

        File.interface.send_upload_request(local_path=local_path, upload_url=url)
        return File.Item(r)

    @staticmethod
    def modify(
        file_id: str,
        file_name: str,
        category: str = "",
    ) -> Item:
        category_id = File.get_category_id_by_name(category)
        payload = {
            "fileName": file_name,
            "categoryId": category_id,
        }
        r = File.interface.send_request(
            rtype=RequestTypes.PATCH,
            route=f"file/{file_id}",
            json=payload,
            overwrite_base_url="https://v2.api.audio/v3",
        )
        return File.Item(r)

    @staticmethod
    def get(file_id: str) -> Item:
        r = File.interface.send_request(
            rtype=RequestTypes.GET,
            route=f"file/{file_id}",
            overwrite_base_url="https://v2.api.audio/v3",
        )
        return File.Item(r)

    @staticmethod
    def delete(file_id: str, folder_id: str) -> APIResponseItem:
        # Needs more thought
        r = File.interface.send_request(
            rtype=RequestTypes.DELETE,
            route=f"file/{file_id}/{folder_id}",
            overwrite_base_url="https://v2.api.audio/v3",
        )
        return APIResponseItem(r)

    @staticmethod
    def get_file_categories() -> APIResponseItem:
        r = File.interface.send_request(
            rtype=RequestTypes.GET,
            route="file/metadata/file-categories",
            overwrite_base_url="https://v2.api.audio/v3",
        )
        return APIResponseItem(r)

    @staticmethod
    def get_category_id_by_name(name: str) -> Optional[UUID]:
        category_id = None
        categories = [
            {"category_id": y["categoryId"], "name": y["name"]}
            for x in File.get_file_categories().data["fileTypes"]
            for y in x["fileCategories"]
        ]
        category_id = next(filter(lambda x: x["name"] == name, categories), None)
        return category_id


class Folder:
    FAMILY = "content"
    interface = RequestInterface(family=FAMILY)

    class Item(APIResponseItem):
        def __init__(self, response: dict) -> None:
            super().__init__(response)
            self.folders = Folder.List(response["folders"], list_type="folders")
            self.files = File.List(response["files"], list_type="files")
            self.current_path_chain = response["currentPathChain"]

    class List(APIResponseList):
        def __init__(self, response: dict, list_type: str) -> None:
            super().__init__(response, list_type)

        def resolve_item(self, list_type: str, item: Any) -> dict:
            if list_type == "folders":
                return {"data": item}
            else:
                raise Exception()

    @staticmethod
    def get_root() -> Item:
        r = Folder.interface.send_request(
            rtype=RequestTypes.GET,
            route="v3/file/folder",
            overwrite_base_url="https://v2.api.audio",
        )
        return Folder.Item(r)

    @staticmethod
    def create(name: str, parent_folder_id: Optional[UUID] = None) -> APIResponseItem:
        folder = {
            "folderName": name,
            "parentFolderId": parent_folder_id,
        }
        r = Folder.interface.send_request(
            rtype=RequestTypes.POST,
            route="file/folder",
            json=folder,
            overwrite_base_url="https://v2.api.audio/v3",
        )
        return APIResponseItem(r)

    @staticmethod
    def get(folder_id: UUID) -> APIResponseItem:
        r = Folder.interface.send_request(
            rtype=RequestTypes.GET,
            route=f"folder/{folder_id}",
            overwrite_base_url="https://v2.api.audio/v3",
        )
        return APIResponseItem(r)

    @staticmethod
    def modify(
        folder_id: UUID,
        name: str,
    ) -> APIResponseItem:
        folder = {
            "folderName": name,
        }
        r = Folder.interface.send_request(
            rtype=RequestTypes.PATCH,
            route=f"folder/{folder_id}",
            json=folder,
            overwrite_base_url="https://v2.api.audio/v3",
        )
        return APIResponseItem(r)

    @staticmethod
    def delete(folder_id: UUID) -> APIResponseItem:
        r = File.interface.send_request(
            rtype=RequestTypes.DELETE,
            route=f"folder/{folder_id}",
            overwrite_base_url="https://v2.api.audio/v3",
        )
        return APIResponseItem(r)
