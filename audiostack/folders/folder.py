from typing import List, Optional
from uuid import UUID

from audiostack.files.file import File
from audiostack.helpers.request_interface import RequestInterface
from audiostack.helpers.request_types import RequestTypes


class Folder:
    """Folder management class for handling folder operations in AudioStack.

    This class provides methods for creating, retrieving, and deleting folders
    in the AudioStack system.
    """

    FAMILY = "folders"
    interface = RequestInterface(family=FAMILY)

    class Item:
        """Represents a folder item in the AudioStack system.

        This class encapsulates folder metadata including ID, name, and
        hierarchy information.
        """

        def __init__(self, response: dict) -> None:
            """Initialize a Folder.Item instance from API response data.

            Args:
                response: Dictionary containing folder metadata from the API.
            """
            self.folderId: str = str(response["folder_id"])
            self.folderName: str = response["folder_name"]
            self.parentFolderId: Optional[str] = (
                str(response.get("parent_folder_id"))
                if response.get("parent_folder_id")
                else None
            )
            self.lastModified: Optional[str] = response.get("last_modified")
            self.createdBy: str = response["created_by"]
            self.createdAt: str = response["created_at"]

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
            self.currentPathChain: List[Folder.Item] = [
                Folder.Item(response=x) for x in response.get("current_path_chain", [])
            ]

    @staticmethod
    def get_root_folder_id() -> str:
        """Get the ID of the root folder.

        Returns:
            str: The unique identifier of the root folder.
        """
        response = Folder.interface.send_request(
            rtype=RequestTypes.GET,
            route="",
        )
        rootFolderId = response["current_path_chain"][0]["folder_id"]
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
            "folder_name": name,
        }

        if parentFolderId:
            payload["parent_folder_id"] = str(parentFolderId)

        r = Folder.interface.send_request(
            rtype=RequestTypes.POST,
            route="",
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
            route=f"{folderId}",
        )
        return Folder.Item(response=r["current_path_chain"][0])

    @staticmethod
    def delete(folderId: UUID) -> None:
        """Delete a folder from AudioStack.

        Args:
            folderId: The unique identifier of the folder to delete.
        """
        Folder.interface.send_request(
            rtype=RequestTypes.DELETE,
            route=f"{folderId}",
        )

    @staticmethod
    def list(path: Optional[str] = None) -> "ListResponse":
        """List files and folders in a directory.

        Args:
            path: Optional path to list. If None, lists root folder.

        Returns:
            ListResponse: Contains folders, files, and current path chain.
        """
        query_params = {}
        if path:
            query_params["path"] = path

        r = Folder.interface.send_request(
            rtype=RequestTypes.GET,
            route="",
            query_parameters=query_params,
        )
        return Folder.ListResponse(response=r)

    @staticmethod
    def search(query: str) -> "ListResponse":
        """Search for files and folders.

        Args:
            query: Search query string.

        Returns:
            ListResponse: Contains matching folders and files.
        """
        r = Folder.interface.send_request(
            rtype=RequestTypes.GET,
            route="search",
            query_parameters={"query": query},
        )
        return Folder.ListResponse(response=r)

    @staticmethod
    def patch(folderId: UUID, folderName: str) -> None:
        """Modify folder name.

        Args:
            folderId: The unique identifier of the folder to modify.
            folderName: New name for the folder.
        """
        payload = {
            "folder_name": folderName,
        }

        Folder.interface.send_request(
            rtype=RequestTypes.PATCH,
            route=f"{folderId}",
            json=payload,
        )
