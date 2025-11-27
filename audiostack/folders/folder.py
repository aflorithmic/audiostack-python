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
        """Represents a folder item in the AudioStack system."""

        def __init__(self, response: dict) -> None:
            if "statusCode" in response and "folderId" not in response:
                error_msg = response.get("message", "Unknown error")
                status_code = response.get("statusCode", "unknown")
                raise Exception(
                    f"Error response received (status {status_code}): {error_msg}"
                )

            self.folderId: str = str(response["folderId"])
            self.folderName: str = response["folderName"]
            parent_folder_id = response.get("parentFolderId")
            self.parentFolderId: Optional[str] = (
                str(parent_folder_id) if parent_folder_id is not None else None
            )
            self.createdBy: str = response["createdBy"]
            self.createdAt: str = response["createdAt"]
            self.updatedAt: Optional[str] = response.get("updatedAt")
            self.updatedBy: Optional[str] = response.get("updatedBy")

    class ListResponse:
        """Represents a list response containing folders and files.

        This class encapsulates the response from folder listing operations,
        containing both folder and file items along with path chain
        information and pagination details.
        """

        def __init__(self, response: dict) -> None:
            if isinstance(response, dict) and "data" in response:
                data = response["data"]
                pagination = response.get("pagination", {})
            else:
                data = response
                pagination = {}

            self.folders: List[Folder.Item] = [
                Folder.Item(response=x) for x in data.get("folders", [])
            ]
            self.files: List[File.Item] = [
                File.Item(response=x) for x in data.get("files", [])
            ]
            current_path_chain = data.get("currentPathChain", [])
            self.currentPathChain: List[Folder.Item] = [
                Folder.Item(response=x) for x in current_path_chain
            ]

            self.pagination: Optional[dict] = pagination if pagination else None
            self.limit: Optional[int] = pagination.get("limit") if pagination else None
            self.offset: Optional[int] = (
                pagination.get("offset") if pagination else None
            )

    class FilesListResponse:
        """Represents a paginated list of files in a folder."""

        def __init__(self, response: dict) -> None:
            if isinstance(response, dict) and "data" in response:
                files_data = response["data"]
                pagination = response.get("pagination", {})
            else:
                files_data = response if isinstance(response, list) else []
                pagination = {}

            self.files: List[File.Item] = [File.Item(response=x) for x in files_data]
            self.pagination: Optional[dict] = pagination if pagination else None
            self.limit: Optional[int] = pagination.get("limit") if pagination else None
            self.offset: Optional[int] = (
                pagination.get("offset") if pagination else None
            )

    class SearchResponse:
        """Represents a search response containing folders and files.

        This class is specifically for search operations and contains
        only folders and files, without currentPathChain.
        """

        def __init__(self, response: dict) -> None:
            if isinstance(response, dict) and "data" in response:  # handle pagination
                data = response["data"]
            else:
                data = response

            self.folders: List[Folder.Item] = [
                Folder.Item(response=x) for x in data.get("folders", [])
            ]
            self.files: List[File.Item] = [
                File.Item(response=x) for x in data.get("files", [])
            ]

    @staticmethod
    def get_root_folder_id() -> str:
        response = Folder.interface.send_request(
            rtype=RequestTypes.GET,
            route="",
        )
        # Handle paginated response structure
        if isinstance(response, dict) and "data" in response:
            data = response["data"]
            current_path_chain = data.get("currentPathChain", [])
        else:
            current_path_chain = response.get("currentPathChain", [])

        if current_path_chain:
            root_folder = current_path_chain[0]
            rootFolderId = root_folder.get("folderId")
            if rootFolderId:
                return str(rootFolderId)
        raise Exception("Root folder not found in response")

    @staticmethod
    def create(name: str, parentFolderId: Optional[UUID] = None) -> "Folder.Item":
        """Create a new folder in AudioStack.

        Args:
            name: The name of the folder to create.
            parentFolderId: Optional UUID of the parent folder. If None,
                creates in root.
        """
        payload = {
            "folder_name": name,
        }

        if parentFolderId:
            payload["parent_folder_id"] = str(parentFolderId)
            # Debug: verify the UUID string format
            print(
                f"DEBUG: Creating folder with parent_folder_id: {payload['parent_folder_id']}"
            )

        r = Folder.interface.send_request(
            rtype=RequestTypes.POST,
            route="",
            json=payload,
        )
        return Folder.Item(response=r)

    @staticmethod
    def get(
        folderId: UUID,
        filter: Optional[str] = None,
        orderBy: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> "ListResponse":
        """Retrieve a folder by its ID and list its contents.

        Args:
            folderId: The unique identifier of the folder to retrieve.
            filter: Optional OData $filter expression for filtering files.
            orderBy: Optional OData $orderBy expression for sorting.
            limit: Optional limit for pagination (number of items per page).
            offset: Optional offset for pagination (number of items to skip).

        Returns:
            ListResponse: A list response containing folders, files,
                and path chain with pagination.
        """
        query_params: dict[str, str | int] = {}
        if filter:
            query_params["$filter"] = filter
        if orderBy:
            query_params["$orderBy"] = orderBy
        if limit is not None:
            query_params["limit"] = limit
        if offset is not None:
            query_params["offset"] = offset

        r = Folder.interface.send_request(
            rtype=RequestTypes.GET,
            route=f"{folderId}",
            query_parameters=query_params if query_params else None,
        )
        return Folder.ListResponse(response=r)

    @staticmethod
    def delete(folderId: UUID) -> str:
        Folder.interface.send_request(
            rtype=RequestTypes.DELETE,
            route=f"{folderId}",
        )
        return f"Folder {folderId} deleted successfully"

    @staticmethod
    def list(
        path: Optional[str] = None,
        filter: Optional[str] = None,
        orderBy: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> "ListResponse":
        """List files and folders in a directory.

        Args:
            path: Optional path to list. If None, lists root folder.
            filter: Optional OData $filter expression for filtering files.
            orderBy: Optional OData $orderBy expression for sorting.
            limit: Optional limit for pagination (number of items per page).
            offset: Optional offset for pagination (number of items to skip).

        Returns:
            ListResponse: A list response containing folders, files,
                and path chain with pagination.
        """
        query_params: dict[str, str | int] = {}
        if path:
            query_params["path"] = path
        if filter:
            query_params["$filter"] = filter
        if orderBy:
            query_params["$orderBy"] = orderBy
        if limit is not None:
            query_params["limit"] = limit
        if offset is not None:
            query_params["offset"] = offset

        r = Folder.interface.send_request(
            rtype=RequestTypes.GET,
            route="",
            query_parameters=query_params if query_params else None,
        )
        return Folder.ListResponse(response=r)

    @staticmethod
    def search(query: str) -> "SearchResponse":
        """Search for files and folders.

        Args:
            query: Search query string.

        Returns:
            SearchResponse: Contains matching folders and files.
        """
        r = Folder.interface.send_request(
            rtype=RequestTypes.GET,
            route="search",
            query_parameters={"query": query},
        )
        return Folder.SearchResponse(response=r)

    @staticmethod
    def patch(folderId: UUID, folderName: str) -> "Folder.Item":
        """Modify folder name.

        Args:
            folderId: The unique identifier of the folder to modify.
            folderName: New name for the folder.
        """
        payload = {
            "folder_name": folderName,
        }

        r = Folder.interface.send_request(
            rtype=RequestTypes.PATCH,
            route=f"{folderId}",
            json=payload,
        )
        return Folder.Item(response=r)

    @staticmethod
    def list_files(
        folderId: UUID,
        filter: Optional[str] = None,
        orderBy: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> "FilesListResponse":
        """List files in a folder.

        Args:
            folderId: The unique identifier of the folder.
            filter: Optional OData $filter expression for filtering files.
            orderBy: Optional OData $orderBy expression for sorting.
            limit: Optional limit for pagination (number of items per page).
            offset: Optional offset for pagination (number of items to skip).

        Returns:
            FilesListResponse: A list response containing files with pagination.
        """
        query_params: dict[str, str | int] = {}
        if filter:
            query_params["$filter"] = filter
        if orderBy:
            query_params["$orderBy"] = orderBy
        if limit is not None:
            query_params["limit"] = limit
        if offset is not None:
            query_params["offset"] = offset

        r = Folder.interface.send_request(
            rtype=RequestTypes.GET,
            route=f"{folderId}/files",
            query_parameters=query_params if query_params else None,
        )

        return Folder.FilesListResponse(response=r)

    class StatsResponse:
        def __init__(self, response: dict) -> None:
            self.folderId: str = str(response["folderId"])
            self.fileTypes: List[dict] = response.get("fileTypes", [])

    @staticmethod
    def get_stats(
        folderId: UUID,
    ) -> (
        "StatsResponse"
    ):  # todo check what get_stats returns - is it wrapped in a 'data' object? if so, fix
        """Get folder statistics.

        Args:
            folderId: The unique identifier of the folder.

        Returns:
            StatsResponse: Folder statistics including file type counts.
        """
        r = Folder.interface.send_request(
            rtype=RequestTypes.GET,
            route=f"{folderId}/stats",
        )
        return Folder.StatsResponse(response=r)
