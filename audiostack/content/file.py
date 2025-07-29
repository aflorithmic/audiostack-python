import os
import time
from typing import List, Optional
from uuid import UUID

from audiostack import TIMEOUT_THRESHOLD_S
from audiostack.helpers.request_interface import RequestInterface
from audiostack.helpers.request_types import RequestTypes


class File:
    """File management class for handling file operations in AudioStack.

    This class provides methods for creating, retrieving, and deleting files
    in the AudioStack system.
    """

    FAMILY = "v3"
    interface = RequestInterface(family=FAMILY)

    class Item:
        """Represents a file item in the AudioStack system.

        This class encapsulates file metadata and provides methods for
        file operations like downloading.
        """

        def __init__(self, response: dict) -> None:
            """Initialize a File.Item instance from API response data.

            Args:
                response: Dictionary containing file metadata from the API.
            """
            self.fileId: str = response["fileId"]
            self.fileName: str = response["fileName"]
            self.url: str = response.get("url", "")
            self.createdBy: str = response.get("createdBy", "")
            self.lastModified: str = response.get("lastModified", "")
            self.fileType: dict = response.get("fileType", {})
            self.fileCategory: Optional[str] = response.get("fileCategory", None)
            self.size: str = str(response.get("size", ""))
            self.createdAt: str = response.get("createdAt", "")
            self.status: str = response.get("status", "")
            self.duration: Optional[str] = response.get("duration", None)

        def download(self, fileName: str, path: str = "./") -> None:
            """Download the file to the specified local path.

            Args:
                fileName: Name to save the file as locally.
                path: Directory path where the file should be saved. Defaults to "./".

            Raises:
                Exception: If no URL is available for the file.
            """
            if not self.url:
                raise Exception(
                    "No URL found for this file. Please check the file has been processed."
                )
            RequestInterface.download_url(url=self.url, destination=path, name=fileName)

    @staticmethod
    def get(fileId: str) -> Item:
        """Retrieve a file by its ID.

        Args:
            fileId: The unique identifier of the file to retrieve.

        Returns:
            File.Item: A file item containing the file metadata.
        """
        r = File.interface.send_request(
            rtype=RequestTypes.GET,
            route=f"file/{fileId}",
        )
        return File.Item(response=r)

    @staticmethod
    def create(
        localPath: str,
        uploadPath: str,
        folderId: Optional[UUID] = None,
    ) -> Item:
        """Create and upload a new file to AudioStack.

        This method uploads a local file to the AudioStack system and waits
        for the upload to complete before returning the file item.

        Args:
            localPath: Path to the local file to upload.
            uploadPath: Name to assign to the file in AudioStack.
            folderId: Optional UUID of the folder to upload to. If None, uses root folder.

        Returns:
            File.Item: The created file item with complete metadata.

        Raises:
            Exception: If localPath is not provided, file doesn't exist, uploadPath is not provided,
                      or if the upload fails.
        """
        if not localPath:
            raise Exception("Please supply a localPath (path to your local file)")

        if not os.path.isfile(localPath):
            raise Exception("Supplied file does not exist")

        if not uploadPath:
            raise Exception("Please supply a valid file name")

        payload = {
            "fileName": uploadPath,
            "folderId": folderId,
        }

        r = File.interface.send_request(
            rtype=RequestTypes.POST,
            route="file/create-upload-url",
            json=payload,
        )
        File.interface.send_upload_request(
            local_path=localPath, upload_url=r["uploadUrl"], mime_type=r["mimeType"]
        )

        start = time.time()

        file = File.get(fileId=r["fileId"])

        while file.status != "uploaded" and time.time() - start < TIMEOUT_THRESHOLD_S:
            print("Response in progress please wait...")
            file = File.get(fileId=r["fileId"])

        if file.status != "uploaded":
            raise Exception("File upload failed")

        return file

    @staticmethod
    def delete(fileId: str, folderId: str = "") -> None:
        """Delete a file from AudioStack.

        Args:
            fileId: The unique identifier of the file to delete.
            folderId: The folder ID where the file is located. If empty, uses root folder.
        """
        if not folderId:
            folderId = Folder.get_root_folder_id()

        File.interface.send_request(
            rtype=RequestTypes.DELETE,
            route=f"file/{fileId}/{folderId}",
        )


class Folder:
    """Folder management class for handling folder operations in AudioStack.

    This class provides methods for creating, retrieving, and deleting folders
    in the AudioStack system.
    """

    FAMILY = "v3"
    interface = RequestInterface(family=FAMILY)

    class Item:
        """Represents a folder item in the AudioStack system.

        This class encapsulates folder metadata including ID, name, and hierarchy information.
        """

        def __init__(self, response: dict) -> None:
            """Initialize a Folder.Item instance from API response data.

            Args:
                response: Dictionary containing folder metadata from the API.
            """
            self.folderId: str = response["folderId"]
            self.folderName: str = response["folderName"]
            self.parentFolderId: str = response.get("parentFolderId", "")
            self.createdBy: str = response.get("createdBy", "")
            self.lastModified: Optional[str] = response.get("lastModified", None)
            self.createdAt: str = response.get("createdAt", "")

    class ListResponse:
        """Represents a list response containing folders and files.

        This class encapsulates the response from folder listing operations,
        containing both folder and file items along with path chain information.
        """

        def __init__(self, response: dict) -> None:
            """Initialize a ListResponse instance from API response data.

            Args:
                response: Dictionary containing folder listing data from the API.
            """
            self.folders: List[Folder.Item] = [
                Folder.Item(response=x) for x in response["folders"]
            ]
            self.files: List[File.Item] = [
                File.Item(response=x) for x in response["files"]
            ]
            self.currentPathChain: dict = response["currentPathChain"]

    @staticmethod
    def get_root_folder_id() -> str:
        """Get the ID of the root folder.

        Returns:
            str: The unique identifier of the root folder.
        """
        rootFolderId = Folder.interface.send_request(
            rtype=RequestTypes.GET,
            route="folder",
        )["currentPathChain"][0]["folderId"]
        return rootFolderId

    @staticmethod
    def create(name: str, parentFolderId: Optional[UUID] = None) -> "Folder.Item":
        """Create a new folder in AudioStack.

        Args:
            name: The name of the folder to create.
            parentFolderId: Optional UUID of the parent folder. If None, creates in root.

        Returns:
            Folder.Item: The created folder item with complete metadata.
        """
        payload = {
            "folderName": name,
        }

        if parentFolderId:
            payload["parentFolderId"] = str(parentFolderId)

        r = Folder.interface.send_request(
            rtype=RequestTypes.POST,
            route="folder",
            json=payload,
        )
        return Folder.Item(response=r)

    @staticmethod
    def get(folderId: UUID) -> "Folder.Item":
        """Retrieve a folder by its ID.

        Args:
            folderId: The unique identifier of the folder to retrieve.

        Returns:
            Folder.Item: A folder item containing the folder metadata.
        """
        r = Folder.interface.send_request(
            rtype=RequestTypes.GET,
            route=f"folder/{folderId}",
        )
        return Folder.Item(response=r["currentPathChain"][0])

    @staticmethod
    def delete(folderId: UUID) -> None:
        """Delete a folder from AudioStack.

        Args:
            folderId: The unique identifier of the folder to delete.
        """
        File.interface.send_request(
            rtype=RequestTypes.DELETE,
            route=f"folder/{folderId}",
        )
