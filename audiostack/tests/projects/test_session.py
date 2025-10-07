"""
Comprehensive test suite for AudioStack Session functionality.

This module provides both integration tests (against real API) and unit tests
(with mocked responses) for the Session class.
"""

import os
import random
from typing import Any, Generator
from unittest.mock import patch
from uuid import UUID

import pytest

import audiostack
from audiostack.projects.project import Project, Session
from audiostack.tests.utils import (
    create_test_project_name,
    create_test_session_name,
)

# Configure AudioStack for integration tests
audiostack.api_base = os.environ.get("AUDIO_STACK_DEV_URL", "https://v2.api.audio")
audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]  # type: ignore


# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture
def test_project() -> Generator[Project.Item, None, None]:
    """Create a test project for session testing."""
    project_name = create_test_project_name()
    project = Project.create(projectName=project_name)
    yield project


@pytest.fixture
def test_session(test_project: Project.Item) -> Generator[Session.Item, None, None]:
    """Create a test session for testing."""
    workflow_id = f"workflow_{random.randint(1000, 9999)}"
    session_name = create_test_session_name()
    status = "active"
    state = {"key1": "value1", "key2": "value2"}

    session = Session.create(
        projectId=UUID(test_project.projectId),
        workflowId=workflow_id,
        sessionName=session_name,
        status=status,
        state=state,
    )
    yield session
    try:
        Session.delete(
            projectId=UUID(test_project.projectId), sessionId=UUID(session.sessionId)
        )
    except Exception:
        pass


@pytest.fixture
def mock_session_response() -> dict:
    """Mock session response data for unit tests."""
    return {
        "sessionId": "12345678-1234-5678-9abc-123456789012",
        "sessionName": "test_session",
        "status": "active",
        "workflowId": "test_workflow",
        "projectId": "87654321-4321-8765-cba9-876543210987",
        "createdBy": "user123",
        "createdAt": "2024-01-01T12:00:00Z",
        "state": {"key": "value"},
        "lastModifiedBy": None,
        "lastModified": None,
        "audioformId": None,
    }


@pytest.fixture
def mock_session_list_response() -> list[dict]:
    """Mock session list response data for unit tests."""
    return [
        {
            "sessionId": "11111111-1111-1111-1111-111111111111",
            "sessionName": "session1",
            "status": "active",
            "workflowId": "workflow1",
            "projectId": "87654321-4321-8765-cba9-876543210987",
            "createdBy": "user123",
            "createdAt": "2024-01-01T12:00:00Z",
            "state": {"key1": "value1"},
            "lastModifiedBy": None,
            "lastModified": None,
            "audioformId": None,
        },
        {
            "sessionId": "22222222-2222-2222-2222-222222222222",
            "sessionName": "session2",
            "status": "completed",
            "workflowId": "workflow2",
            "projectId": "87654321-4321-8765-cba9-876543210987",
            "createdBy": "user123",
            "createdAt": "2024-01-01T13:00:00Z",
            "state": {"key2": "value2"},
            "lastModifiedBy": "user123",
            "lastModified": "2024-01-01T14:00:00Z",
            "audioformId": "33333333-3333-3333-3333-333333333333",
        },
    ]


# ============================================================================
# UNIT TESTS
# ============================================================================


@pytest.mark.unit
class TestSessionUnit:
    """Unit tests for Session class with mocked API responses."""

    @patch("audiostack.helpers.request_interface.RequestInterface.send_request")
    def test_create(self, mock_send_request: Any, mock_session_response: dict) -> None:
        """Test session creation with mocked response."""
        mock_send_request.return_value = mock_session_response

        session = Session.create(
            projectId=UUID("87654321-4321-8765-cba9-876543210987"),
            workflowId="test_workflow",
            sessionName="test_session",
            status="active",
            state={"key": "value"},
        )

        mock_send_request.assert_called_once()
        call_args = mock_send_request.call_args
        expected_route = "87654321-4321-8765-cba9-876543210987/sessions"
        assert call_args[1]["route"] == expected_route
        assert call_args[1]["json"]["workflow_id"] == "test_workflow"
        assert call_args[1]["json"]["session_name"] == "test_session"

        assert session.sessionId == "12345678-1234-5678-9abc-123456789012"
        assert session.sessionName == "test_session"
        assert session.status == "active"
        assert session.workflowId == "test_workflow"
        assert session.state == {"key": "value"}

    @patch("audiostack.helpers.request_interface.RequestInterface.send_request")
    def test_create_with_audioform(
        self, mock_send_request: Any, mock_session_response: dict
    ) -> None:
        """Test session creation with audioform ID."""
        mock_send_request.return_value = mock_session_response

        audioform_id = UUID("33333333-3333-3333-3333-333333333333")
        Session.create(
            projectId=UUID("87654321-4321-8765-cba9-876543210987"),
            workflowId="test_workflow",
            sessionName="test_session",
            status="active",
            state={"key": "value"},
            audioformId=audioform_id,
        )

        call_args = mock_send_request.call_args
        assert call_args[1]["json"]["audioform_id"] == str(audioform_id)

    @patch("audiostack.helpers.request_interface.RequestInterface.send_request")
    def test_get(self, mock_send_request: Any, mock_session_response: dict) -> None:
        """Test session retrieval with mocked response."""
        mock_send_request.return_value = mock_session_response

        session = Session.get(
            projectId=UUID("87654321-4321-8765-cba9-876543210987"),
            sessionId=UUID("12345678-1234-5678-9abc-123456789012"),
        )

        mock_send_request.assert_called_once()
        call_args = mock_send_request.call_args
        expected_route = (
            "87654321-4321-8765-cba9-876543210987/sessions/"
            "12345678-1234-5678-9abc-123456789012"
        )
        assert call_args[1]["route"] == expected_route

        assert session.sessionId == "12345678-1234-5678-9abc-123456789012"
        assert session.sessionName == "test_session"

    @patch("audiostack.helpers.request_interface.RequestInterface.send_request")
    def test_list(
        self, mock_send_request: Any, mock_session_list_response: list[dict]
    ) -> None:
        """Test session listing with mocked response."""
        mock_send_request.return_value = mock_session_list_response

        sessions = Session.list(projectId=UUID("87654321-4321-8765-cba9-876543210987"))

        mock_send_request.assert_called_once()
        call_args = mock_send_request.call_args
        expected_route = "87654321-4321-8765-cba9-876543210987/sessions"
        assert call_args[1]["route"] == expected_route

        assert len(sessions.sessions) == 2
        assert sessions.sessions[0].sessionName == "session1"
        assert sessions.sessions[1].sessionName == "session2"

    @patch("audiostack.helpers.request_interface.RequestInterface.send_request")
    def test_list_with_workflow_filter(
        self, mock_send_request: Any, mock_session_list_response: list[dict]
    ) -> None:
        """Test session listing with workflow filter."""
        mock_send_request.return_value = mock_session_list_response

        Session.list(
            projectId=UUID("87654321-4321-8765-cba9-876543210987"),
            workflowId="workflow1",
        )

        call_args = mock_send_request.call_args
        assert call_args[1]["query_parameters"]["workflowId"] == "workflow1"

    @patch("audiostack.helpers.request_interface.RequestInterface.send_request")
    def test_update(self, mock_send_request: Any, mock_session_response: dict) -> None:
        """Test session update with mocked response."""
        mock_send_request.return_value = mock_session_response

        Session.update(
            projectId=UUID("87654321-4321-8765-cba9-876543210987"),
            sessionId=UUID("12345678-1234-5678-9abc-123456789012"),
            sessionName="updated_session",
            status="completed",
        )

        mock_send_request.assert_called_once()
        call_args = mock_send_request.call_args
        expected_route = (
            "87654321-4321-8765-cba9-876543210987/sessions/"
            "12345678-1234-5678-9abc-123456789012"
        )
        assert call_args[1]["route"] == expected_route
        assert call_args[1]["json"]["session_name"] == "updated_session"
        assert call_args[1]["json"]["status"] == "completed"

    @patch("audiostack.helpers.request_interface.RequestInterface.send_request")
    def test_delete(self, mock_send_request: Any) -> None:
        """Test session deletion with mocked response."""
        mock_send_request.return_value = {"statusCode": 200}

        Session.delete(
            projectId=UUID("87654321-4321-8765-cba9-876543210987"),
            sessionId=UUID("12345678-1234-5678-9abc-123456789012"),
        )

        mock_send_request.assert_called_once()
        call_args = mock_send_request.call_args
        expected_route = (
            "87654321-4321-8765-cba9-876543210987/sessions/"
            "12345678-1234-5678-9abc-123456789012"
        )
        assert call_args[1]["route"] == expected_route

    def test_session_item_initialisation(self, mock_session_response: dict) -> None:
        """Test Session.Item initialisation with various response formats."""
        # Test with all fields present
        session = Session.Item(mock_session_response)
        assert session.sessionId == "12345678-1234-5678-9abc-123456789012"
        assert session.sessionName == "test_session"
        assert session.audioformId is None

        # Test with audioformId present
        response_with_audioform = mock_session_response.copy()
        audioform_id = "33333333-3333-3333-3333-333333333333"
        response_with_audioform["audioformId"] = audioform_id
        session_with_audioform = Session.Item(response_with_audioform)
        assert session_with_audioform.audioformId == audioform_id

    def test_session_list_response_initialisation(
        self, mock_session_list_response: list[dict]
    ) -> None:
        """Test Session.ListResponse initialisation."""
        sessions = Session.ListResponse(mock_session_list_response)
        assert len(sessions.sessions) == 2
        assert isinstance(sessions.sessions[0], Session.Item)
        assert sessions.sessions[0].sessionName == "session1"
        assert sessions.sessions[1].sessionName == "session2"


# ============================================================================
# INTEGRATION TESTS
# ============================================================================


@pytest.mark.integration
class TestSessionIntegration:
    """Integration tests for Session class against real AudioStack API.

    Focuses on high-value scenarios that can't be adequately tested with mocks:
    - API error handling and edge cases
    - Real API response format validation
    - Complex filtering and bulk operations
    """

    def test_crud_workflow(self, test_project: Project.Item) -> None:
        """Test complete CRUD workflow against real API."""
        # CREATE
        session_name = create_test_session_name()
        workflow_id = f"workflow_{random.randint(1000, 9999)}"
        status = "active"
        state = {"key1": "value1", "key2": "value2"}

        session = Session.create(
            projectId=UUID(test_project.projectId),
            workflowId=workflow_id,
            sessionName=session_name,
            status=status,
            state=state,
        )

        assert session.sessionName == session_name
        assert session.workflowId == workflow_id
        assert session.status == status
        assert session.state == state
        assert session.projectId == test_project.projectId
        assert session.sessionId is not None
        assert session.createdBy is not None
        assert session.createdAt is not None

        # READ
        retrieved_session = Session.get(
            projectId=UUID(test_project.projectId),
            sessionId=UUID(session.sessionId),
        )
        assert retrieved_session.sessionId == session.sessionId
        assert retrieved_session.sessionName == session_name

        # UPDATE
        new_name = "updated_test_session"
        new_status = "completed"
        updated_session = Session.update(
            projectId=UUID(test_project.projectId),
            sessionId=UUID(session.sessionId),
            sessionName=new_name,
            status=new_status,
        )
        assert updated_session.sessionName == new_name
        assert updated_session.status == new_status

        final_session = Session.get(
            projectId=UUID(test_project.projectId),
            sessionId=UUID(session.sessionId),
        )
        assert final_session.sessionName == new_name
        assert final_session.status == new_status

        # DELETE
        Session.delete(
            projectId=UUID(test_project.projectId),
            sessionId=UUID(session.sessionId),
        )

        with pytest.raises(Exception):
            Session.get(
                projectId=UUID(test_project.projectId),
                sessionId=UUID(session.sessionId),
            )

    def test_error_handling(self, test_project: Project.Item) -> None:
        """Test error handling against real API."""
        # Test getting non-existent session
        with pytest.raises(Exception):
            Session.get(
                projectId=UUID(test_project.projectId),
                sessionId=UUID("00000000-0000-0000-0000-000000000000"),
            )

        # Test creating session with invalid project ID
        with pytest.raises(Exception):
            Session.create(
                projectId=UUID("00000000-0000-0000-0000-000000000000"),
                workflowId="test_workflow",
                sessionName="test_session",
                status="active",
                state={},
            )
