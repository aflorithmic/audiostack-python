from typing import Any, Dict, List, Optional
from uuid import UUID

from audiostack.helpers.request_interface import RequestInterface
from audiostack.helpers.request_types import RequestTypes


class Project:
    """Project management class for handling project operations in AudioStack.

    This class provides methods for creating, retrieving, and deleting projects
    in the AudioStack system.
    """

    FAMILY = "projects"
    interface = RequestInterface(family=FAMILY)

    class Item:
        """Represents a project item in the AudioStack system."""

        def __init__(self, response: dict) -> None:
            self.projectId: str = str(response["projectId"])
            self.projectName: str = response["projectName"]
            self.folderId: str = str(response["folderId"])
            self.createdBy: str = response["createdBy"]
            self.createdAt: str = response["createdAt"]
            self.lastModified: Optional[str] = response.get("lastModified")

    class ListResponse:
        """Represents a list response containing projects."""

        def __init__(self, response: List[dict]) -> None:
            self.projects: List[Project.Item] = [
                Project.Item(response=x) for x in response
            ]

    @staticmethod
    def get(projectId: UUID) -> Item:
        r = Project.interface.send_request(
            rtype=RequestTypes.GET,
            route=f"{projectId}",
        )
        return Project.Item(response=r)

    @staticmethod
    def create(projectName: str) -> Item:
        payload = {
            "project_name": projectName,
        }

        r = Project.interface.send_request(
            rtype=RequestTypes.POST,
            route="",
            json=payload,
        )
        return Project.Item(response=r)

    @staticmethod
    def list() -> ListResponse:
        r = Project.interface.send_request(
            rtype=RequestTypes.GET,
            route="",
        )

        # Handle case where response only contains status code (e.g. 204)
        if isinstance(r, dict) and "statusCode" in r and len(r) == 1:
            projects_data = []
        elif isinstance(r, dict) and "data" in r:
            # API returns {"data": [...], "pagination": {...}}
            projects_data = r["data"]
        else:
            # Response is already a list
            projects_data = r
        return Project.ListResponse(response=projects_data)


class Session:
    """Session management class for handling session operations in AudioStack.

    This class provides methods for creating, retrieving, updating, and
    deleting sessions in the AudioStack system.
    """

    FAMILY = "projects"
    interface = RequestInterface(family=FAMILY)

    class Item:
        """Represents a session item in the AudioStack system."""

        def __init__(self, response: dict) -> None:
            """Initialise a Session.Item instance from API response data."""
            self.sessionId: str = str(response["sessionId"])
            self.sessionName: str = response["sessionName"]
            self.status: str = response["status"]
            self.workflowId: str = response["workflowId"]
            self.projectId: str = str(response["projectId"])
            self.createdBy: str = response["createdBy"]
            self.createdAt: str = response["createdAt"]
            self.state: Dict[str, Any] = response["state"]
            self.lastModifiedBy: Optional[str] = response.get("lastModifiedBy")
            self.lastModified: Optional[str] = response.get("lastModified")
            self.audioformId: Optional[str] = (
                str(response["audioformId"])
                if response.get("audioformId") is not None
                else None
            )

    class ListResponse:
        """Represents a list response containing sessions."""

        def __init__(self, response: List[dict]) -> None:
            self.sessions: List[Session.Item] = [
                Session.Item(response=x) for x in response
            ]

    @staticmethod
    def create(
        projectId: UUID,
        workflowId: str,
        sessionName: str,
        status: str,
        state: Dict[str, Any],
        audioformId: Optional[UUID] = None,
    ) -> Item:
        """Create a new session in AudioStack.

        Args:
            projectId: The unique identifier of the project to create the
                session in.
            workflowId: The workflow ID for the session.
            sessionName: The name of the session to create.
            status: The status of the session.
            state: The state data for the session.
            audioformId: Optional audioform ID to associate with the session.

        Returns:
            Session.Item: The created session item with complete metadata.
        """
        payload = {
            "workflow_id": workflowId,
            "session_name": sessionName,
            "status": status,
            "state": state,
        }

        if audioformId is not None:
            payload["audioform_id"] = str(audioformId)

        r = Session.interface.send_request(
            rtype=RequestTypes.POST,
            route=f"{projectId}/sessions",
            json=payload,
        )
        return Session.Item(response=r)

    @staticmethod
    def get(projectId: UUID, sessionId: UUID) -> Item:
        r = Session.interface.send_request(
            rtype=RequestTypes.GET,
            route=f"{projectId}/sessions/{sessionId}",
        )
        return Session.Item(response=r)

    @staticmethod
    def list(
        projectId: UUID,
        workflowId: Optional[str] = None,
    ) -> ListResponse:
        query_parameters = {}
        if workflowId is not None:
            query_parameters["workflowId"] = workflowId

        r = Session.interface.send_request(
            rtype=RequestTypes.GET,
            route=f"{projectId}/sessions",
            query_parameters=query_parameters,
        )

        # Handle case where response only contains status code (e.g. 204)
        if isinstance(r, dict) and "statusCode" in r and len(r) == 1:
            sessions_data = []
        elif isinstance(r, dict) and "data" in r:
            # API returns {"data": [...], "pagination": {...}}
            sessions_data = r["data"]
        else:
            # Response is already a list
            sessions_data = r
        return Session.ListResponse(response=sessions_data)

    @staticmethod
    def update(
        projectId: UUID,
        sessionId: UUID,
        sessionName: Optional[str] = None,
        status: Optional[str] = None,
        state: Optional[Dict[str, Any]] = None,
        audioformId: Optional[UUID] = None,
    ) -> Item:
        payload: Dict[str, Any] = {}
        if sessionName is not None:
            payload["session_name"] = sessionName
        if status is not None:
            payload["status"] = status
        if state is not None:
            payload["state"] = state
        if audioformId is not None:
            payload["audioform_id"] = str(audioformId)

        r = Session.interface.send_request(
            rtype=RequestTypes.PATCH,
            route=f"{projectId}/sessions/{sessionId}",
            json=payload,
        )
        return Session.Item(response=r)

    @staticmethod
    def delete(projectId: UUID, sessionId: UUID) -> None:
        Session.interface.send_request(
            rtype=RequestTypes.DELETE,
            route=f"{projectId}/sessions/{sessionId}",
        )
