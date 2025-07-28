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
    FAMILY = "v3"
    interface = RequestInterface(family=FAMILY)

    class Item:
        def __init__(self, response: dict) -> None:
            self.file_id: str = response["fileId"]
            self.file_name: str = response["fileName"]
            self.url: str = response.get("url", "")
            self.created_by: str = response.get("createdBy", "")
            self.last_modified: str = response.get("lastModified", "")
            self.file_type: dict = response.get("fileType", {})
            self.file_category: Optional[str] = response.get("fileCategory", None)
            self.size: str = str(response.get("size", ""))
            self.created_at: str = response.get("createdAt", "")
            self.status: str = response.get("status", "")
            self.duration: Optional[str] = response.get("duration", None)

        def download(self, fileName: str, path: str = "./") -> None:
            if not self.url:
                raise Exception(
                    "No URL found for this file. Please check the file has been processed."
                )
            RequestInterface.download_url(url=self.url, destination=path, name=fileName)

    @staticmethod
    def get(file_id: str) -> Item:
        r = File.interface.send_request(
            rtype=RequestTypes.GET,
            route=f"file/{file_id}",
        )
        return File.Item(response=r)

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

        payload = {
            "fileName": file_name,
            "folderId": folder_id,
        }

        if category:
            payload["categoryId"] = File.get_category_id_by_name(name=category)

        r = File.interface.send_request(
            rtype=RequestTypes.POST,
            route="file/create-upload-url",
            json=payload,
        )
        File.interface.send_upload_request(
            local_path=local_path, upload_url=r["uploadUrl"], mime_type=r["mimeType"]
        )

        start = time.time()

        file = File.get(file_id=r["fileId"])

        while file.status != "uploaded" or time.time() - start >= TIMEOUT_THRESHOLD_S:
            print("Response in progress please wait...")
            file = File.get(file_id=r["fileId"])

        if file.status != "uploaded":
            raise Exception("File upload failed")

        return file

    @staticmethod
    def delete(file_id: str, folder_id: str = "") -> None:
        if not folder_id:
            folder_id = Folder.get_root_folder_id()

        File.interface.send_request(
            rtype=RequestTypes.DELETE,
            route=f"file/{file_id}/{folder_id}",
        )


class Folder:
    FAMILY = "v3"
    interface = RequestInterface(family=FAMILY)

    class Item:
        def __init__(self, response: dict) -> None:
            self.folder_id: str = response["folderId"]
            self.folder_name: str = response["folderName"]
            self.parent_folder_id: str = response.get("parentFolderId", "")
            self.created_by: str = response.get("createdBy", "")
            self.last_modified: Optional[str] = response.get("lastModified", None)
            self.created_at: str = response.get("createdAt", "")

    class ListResponse:
        def __init__(self, response: dict) -> None:
            self.folders: list[Folder.Item] = [
                Folder.Item(response=x) for x in response["folders"]
            ]
            self.files: list[File.Item] = [
                File.Item(response=x) for x in response["files"]
            ]
            self.current_path_chain: dict = response["currentPathChain"]

    @staticmethod
    def get_root_folder_id() -> str:
        root_folder_id = Folder.interface.send_request(
            rtype=RequestTypes.GET,
            route="folder",
        )["currentPathChain"][0]["folderId"]
        return root_folder_id

    @staticmethod
    def create(name: str, parent_folder_id: Optional[UUID] = None) -> "Folder.Item":
        payload = {
            "folderName": name,
        }

        if parent_folder_id:
            payload["parentFolderId"] = str(parent_folder_id)

        r = Folder.interface.send_request(
            rtype=RequestTypes.POST,
            route="folder",
            json=payload,
        )
        return Folder.Item(response=r)

    @staticmethod
    def get(folder_id: UUID) -> "Folder.Item":
        r = Folder.interface.send_request(
            rtype=RequestTypes.GET,
            route=f"folder/{folder_id}",
        )
        return Folder.Item(response=r["currentPathChain"][0])

    @staticmethod
    def delete(folder_id: UUID) -> None:
        File.interface.send_request(
            rtype=RequestTypes.DELETE,
            route=f"folder/{folder_id}",
        )
