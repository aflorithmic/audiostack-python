import enum
import time
from typing import Optional
from uuid import UUID

from audiostack import TIMEOUT_THRESHOLD_S
from audiostack.helpers.file_path import validate_and_resolve_file_path
from audiostack.helpers.request_interface import RequestInterface
from audiostack.helpers.request_types import RequestTypes


class AccessControl(str, enum.Enum):
    """Access control enum for file visibility."""

    public = "public"
    private = "private"


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
            """Initialise a File.Item instance from API response data.

            Args:
                response: Dictionary containing file metadata from the API.
            """
            self.fileId: str = str(response["fileId"])
            self.fileName: str = response["fileName"]
            self.folderId: str = str(response["folderId"])
            self.url: Optional[str] = response.get("url")
            self.createdBy: str = response["createdBy"]
            self.updatedAt: Optional[str] = response.get("updatedAt")
            self.updatedBy: Optional[str] = response.get("updatedBy")

            file_type = response["fileType"]
            if not isinstance(file_type, dict):
                raise ValueError("fileType must be a dictionary")
            self.fileType: dict = file_type

            file_category = response.get("fileCategory")
            self.fileCategory: Optional[dict] = (
                file_category if isinstance(file_category, dict) else None
            )

            self.size: int = response["size"]
            self.createdAt: str = response["createdAt"]
            self.status: str = response["status"]
            self.duration: Optional[float] = response.get("duration")

            access_control = response["accessControl"]
            try:
                self.accessControl: str = AccessControl(access_control).value
            except ValueError:
                raise ValueError(
                    f"Invalid accessControl value: {access_control}. "
                    f"Must be one of: {[e.value for e in AccessControl]}"
                )

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
                    "No URL found for this file. "
                    "Please check the file has been processed."
                )
            RequestInterface.download_url(url=self.url, destination=path, name=fileName)

    @staticmethod
    def get(fileId: UUID) -> Item:
        """Retrieve a file by its ID.

        Args:
            fileId: The unique file ID.

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
        fileName: str,
        folderId: Optional[UUID] = None,
        categoryId: Optional[UUID] = None,
    ) -> Item:
        """Create and upload a new file to AudioStack.

        Args:
            localPath: Path to the local file to upload.
            fileName: Name to assign to the file.
            folderId: Optional UUID of the folder to upload to. If None, uses
                root folder.
            categoryId: Optional UUID of the file category.

        Returns:
            File.Item: The created file item with complete metadata.

        Raises:
            ValueError: If localPath is not provided, is not a string, or is
                not a valid file path.
            FileNotFoundError: If the file does not exist.
            PermissionError: If the file cannot be read.
        """
        localPath = validate_and_resolve_file_path(localPath)

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
        upload_url = r["uploadUrl"]
        mime_type = r["mimeType"]
        file_id = r["fileId"]

        File.interface.send_upload_request(
            local_path=localPath, upload_url=upload_url, mime_type=mime_type
        )

        start = time.time()

        file = File.get(fileId=UUID(file_id))

        while file.status != "uploaded" and time.time() - start < TIMEOUT_THRESHOLD_S:
            print("Response in progress please wait...")
            time.sleep(0.05)
            file = File.get(fileId=UUID(file_id))

        if file.status != "uploaded":
            return file

        return file

    @staticmethod
    def delete(fileId: UUID) -> None:
        """Delete a file from AudioStack.

        Args:
            fileId: The unique file ID to delete.
        """
        File.interface.send_request(
            rtype=RequestTypes.DELETE,
            route=f"{fileId}",
        )

    @staticmethod
    def copy(fileId: UUID, currentFolderId: UUID, newFolderId: UUID) -> Item:
        """Copy a file to a new folder.

        Args:
            fileId: The unique ID of the file to copy.
            currentFolderId: The UUID of the folder to copy the file from.
            newFolderId: The UUID of the folder to copy the file to.

        Returns:
            File.Item: The new file item with the new file ID.
        """
        payload = {
            "file_id": str(fileId),
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
        fileId: UUID,
        fileName: Optional[str] = None,
        categoryId: Optional[UUID] = None,
        categoryName: Optional[str] = None,
        accessControl: Optional[AccessControl] = None,
    ) -> Item:
        """Patch/update file metadata.

        Args:
            fileId: The unique file ID to update.
            fileName: Optional new name for the file.
            categoryId: Optional new category ID for the file.
            categoryName: Optional new category name for the file.
            accessControl: Optional access control setting (public or private).

        Returns:
            File.Item: The updated file item.
        """
        payload = {}
        if fileName is not None:
            payload["file_name"] = fileName
        if categoryId is not None:
            payload["category_id"] = str(categoryId)
        if categoryName is not None:
            payload["category_name"] = categoryName
        if accessControl is not None:
            payload["access_control"] = accessControl.value

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
