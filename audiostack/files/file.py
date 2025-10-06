import os
import time
from typing import Optional
from uuid import UUID

from audiostack import TIMEOUT_THRESHOLD_S
from audiostack.helpers.request_interface import RequestInterface
from audiostack.helpers.request_types import RequestTypes


class File:
    """File management class for handling file operations in AudioStack.

    This class provides methods for creating, retrieving, and deleting files
    in the AudioStack system.
    """

    FAMILY = "files"
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
            self.fileId: str = str(response["fileId"])  # Hard link
            self.fileName: str = response["fileName"]
            self.folderId: str = str(response["folderId"])
            self.url: Optional[str] = response.get("url")
            self.createdBy: str = response["createdBy"]
            self.lastModified: Optional[str] = response.get("lastModified")
            self.fileType: dict = response["fileType"]
            self.fileCategory: Optional[dict] = response.get("fileCategory")
            self.size: int = response["size"]
            self.createdAt: str = response["createdAt"]
            self.status: str = response["status"]
            self.duration: Optional[float] = response.get("duration")

        def download(self, fileName: str, path: str = "./") -> None:
            """Download the file to the specified local path.

            Args:
                fileName: Name to save the file as locally.
                path: Directory path where the file should be saved.
                    Defaults to "./".

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
        """Retrieve a file by its hard link ID.

        Args:
            fileId: The unique hard link identifier of the file to retrieve.

        Returns:
            File.Item: A file item containing the file metadata.
        """
        r = File.interface.send_request(
            rtype=RequestTypes.GET,
            route=f"{fileId}",
        )
        return File.Item(response=r)

    @staticmethod
    def create(
        localPath: str,
        uploadPath: str,
        fileName: str,
        folderId: Optional[UUID] = None,
        categoryId: Optional[UUID] = None,
    ) -> Item:
        """Create and upload a new file to AudioStack.

        This method uploads a local file to the AudioStack system and waits
        for the upload to complete before returning the file item.

        Args:
            localPath: Path to the local file to upload.
            uploadPath: Name to assign to the file in AudioStack.
            fileName: Name to assign to the file.
            folderId: Optional UUID of the folder to upload to. If None, uses
                root folder.
            categoryId: Optional UUID of the file category.

        Returns:
            File.Item: The created file item with complete metadata.

        Raises:
            Exception: If localPath is not provided, file doesn't exist,
                uploadPath is not provided, or if the upload fails.
        """
        if not localPath:
            raise Exception("Please supply a localPath (path to your local file)")

        if not os.path.isfile(localPath):
            raise Exception("Supplied file does not exist")

        if not uploadPath:
            raise Exception("Please supply a valid file name")

        payload = {
            "file_name": fileName,
            "folder_id": str(folderId) if folderId else None,
            "category_id": str(categoryId) if categoryId else None,
        }

        r = File.interface.send_request(
            rtype=RequestTypes.POST,
            route="",
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
    def delete(fileId: str) -> None:
        """Delete a file from AudioStack.

        Args:
            fileId: The unique hard link identifier of the file to delete.
        """
        File.interface.send_request(
            rtype=RequestTypes.DELETE,
            route=f"{fileId}",
        )

    @staticmethod
    def copy(fileId: str, currentFolderId: UUID, newFolderId: UUID) -> Item:
        """Copy a file to a new folder.

        This creates a new hard link for the file in the specified folder.

        Args:
            fileId: The unique hard link identifier of the file to copy.
            currentFolderId: The UUID of the folder to copy the file from.
            newFolderId: The UUID of the folder to copy the file to.

        Returns:
            File.Item: The new file item with the new hard link ID.
        """
        payload = {
            "file_id": fileId,
            "current_folder_id": str(currentFolderId),
            "new_folder_id": str(newFolderId),
        }

        r = File.interface.send_request(
            rtype=RequestTypes.PUT,
            route="copy",
            json=payload,
        )
        return File.Item(response=r)

    @staticmethod
    def patch(
        fileId: str,
        file_name: Optional[str] = None,
        category_id: Optional[UUID] = None,
        category_name: Optional[str] = None,
    ) -> Item:
        """Patch/update file metadata.

        Args:
            fileId: The unique hard link identifier of the file to update.
            file_name: Optional new name for the file.
            category_id: Optional new category ID for the file.
            category_name: Optional new category name for the file.

        Returns:
            File.Item: The updated file item.
        """
        payload = {}
        if file_name is not None:
            payload["file_name"] = file_name
        if category_id is not None:
            payload["category_id"] = str(category_id)
        if category_name is not None:
            payload["category_name"] = category_name

        r = File.interface.send_request(
            rtype=RequestTypes.PATCH,
            route=f"{fileId}",
            json=payload,
        )
        return File.Item(response=r)

    @staticmethod
    def get_file_categories() -> dict:
        """Get available file categories and types.

        Returns:
            dict: Dictionary containing file types and their categories.
        """
        r = File.interface.send_request(
            rtype=RequestTypes.GET,
            route="file-categories",
        )
        return r


#
