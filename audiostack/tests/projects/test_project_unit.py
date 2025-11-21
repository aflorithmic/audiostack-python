# Temporarily disabled - projects and sessions integration
# This file will be re-enabled in the future
"""
from unittest.mock import MagicMock, patch
from uuid import UUID, uuid4

import pytest

from audiostack.projects.project import Project


# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture
def mock_project_response() -> dict:
    \"\"\"Mock project response for unit testing.\"\"\"
    return {
        "projectId": str(uuid4()),
        "projectName": "Test Project",
        "folderId": str(uuid4()),
        "createdBy": "test-user",
        "createdAt": "2024-01-01T00:00:00Z",
        "lastModified": None,
    }


@pytest.fixture
def mock_projects_list_response() -> list[dict]:
    \"\"\"Mock projects list response for unit testing.\"\"\"
    return [
        {
            "projectId": str(uuid4()),
            "projectName": "Project 1",
            "folderId": str(uuid4()),
            "createdBy": "test-user",
            "createdAt": "2024-01-01T00:00:00Z",
            "lastModified": None,
        },
        {
            "projectId": str(uuid4()),
            "projectName": "Project 2",
            "folderId": str(uuid4()),
            "createdBy": "test-user",
            "createdAt": "2024-01-02T00:00:00Z",
            "lastModified": "2024-01-03T00:00:00Z",
        },
    ]


# ============================================================================
# UNIT TESTS
# ============================================================================


@pytest.mark.unit
def test_project_item_initialisation(mock_project_response: dict) -> None:
    \"\"\"Test Project.Item initialisation with mock data.\"\"\"
    project = Project.Item(response=mock_project_response)

    assert project.projectId == mock_project_response["projectId"]
    assert project.projectName == mock_project_response["projectName"]
    assert project.folderId == mock_project_response["folderId"]
    assert project.createdBy == mock_project_response["createdBy"]
    assert project.createdAt == mock_project_response["createdAt"]
    assert project.lastModified is None


@pytest.mark.unit
def test_project_item_with_last_modified() -> None:
    \"\"\"Test Project.Item with lastModified field.\"\"\"
    response = {
        "projectId": str(uuid4()),
        "projectName": "Test Project",
        "folderId": str(uuid4()),
        "createdBy": "test-user",
        "createdAt": "2024-01-01T00:00:00Z",
        "lastModified": "2024-01-02T00:00:00Z",
    }

    project = Project.Item(response=response)
    assert project.lastModified == "2024-01-02T00:00:00Z"


@pytest.mark.unit
@patch("audiostack.projects.project.Project.interface.send_request")
def test_project_create_success(
    mock_send_request: MagicMock, mock_project_response: dict
) -> None:
    \"\"\"Test successful project creation with mocked response.\"\"\"
    mock_send_request.return_value = mock_project_response

    project = Project.create(projectName="Test Project")

    assert project.projectName == "Test Project"
    assert project.projectId == mock_project_response["projectId"]
    assert project.folderId == mock_project_response["folderId"]
    assert project.createdBy == mock_project_response["createdBy"]
    assert project.createdAt == mock_project_response["createdAt"]


@pytest.mark.unit
@patch("audiostack.projects.project.Project.interface.send_request")
def test_project_get_success(
    mock_send_request: MagicMock, mock_project_response: dict
) -> None:
    \"\"\"Test successful project retrieval with mocked response.\"\"\"
    mock_send_request.return_value = mock_project_response
    project_id = UUID("12345678-1234-5678-9abc-123456789012")

    project = Project.get(projectId=project_id)

    assert project.projectId == mock_project_response["projectId"]
    assert project.projectName == mock_project_response["projectName"]
    assert project.createdBy == mock_project_response["createdBy"]


@pytest.mark.unit
@patch("audiostack.projects.project.Project.interface.send_request")
def test_project_list_success(
    mock_send_request: MagicMock, mock_projects_list_response: list[dict]
) -> None:
    \"\"\"Test successful project listing with mocked response.\"\"\"
    mock_send_request.return_value = mock_projects_list_response

    response = Project.list()

    assert isinstance(response.projects, list)
    assert len(response.projects) == 2
    assert response.projects[0].projectName == "Project 1"
    assert response.projects[1].projectName == "Project 2"


@pytest.mark.unit
@patch("audiostack.projects.project.Project.interface.send_request")
def test_project_create_error_handling(mock_send_request: MagicMock) -> None:
    \"\"\"Test Project.create error handling.\"\"\"
    mock_send_request.side_effect = Exception("422 Validation error")

    with pytest.raises(Exception) as exc_info:
        Project.create(projectName="")
    assert "422" in str(exc_info.value) or "validation" in str(
        exc_info.value
    ).lower()


@pytest.mark.unit
@patch("audiostack.projects.project.Project.interface.send_request")
def test_project_get_error_handling(mock_send_request: MagicMock) -> None:
    \"\"\"Test Project.get error handling.\"\"\"
    mock_send_request.side_effect = Exception("404 Project not found")

    with pytest.raises(Exception) as exc_info:
        Project.get(
            projectId=UUID("00000000-0000-0000-0000-000000000000")
        )
    assert "404" in str(exc_info.value) or "not found" in str(
        exc_info.value
    ).lower()


@pytest.mark.unit
def test_project_list_response_initialisation(
    mock_projects_list_response: list[dict],
) -> None:
    \"\"\"Test Project.ListResponse initialisation.\"\"\"
    response = Project.ListResponse(response=mock_projects_list_response)

    assert len(response.projects) == 2
    assert all(isinstance(p, Project.Item) for p in response.projects)
    assert response.projects[0].projectName == "Project 1"
    assert response.projects[1].projectName == "Project 2"


@pytest.mark.unit
@pytest.mark.parametrize(
    "invalid_name,expected_error",
    [
        ("", "422"),
        ("   ", "422"),
        ("x" * 1000, "422"),
    ],
)
@patch("audiostack.projects.project.Project.interface.send_request")
def test_project_create_validation_errors(
    mock_send_request: MagicMock,
    invalid_name: str,
    expected_error: str,
) -> None:
    \"\"\"Test project creation with invalid names.\"\"\"
    mock_send_request.side_effect = Exception(
        f"{expected_error} Validation error"
    )

    with pytest.raises(Exception) as exc_info:
        Project.create(projectName=invalid_name)
    assert (
        expected_error in str(exc_info.value)
        or "validation" in str(exc_info.value).lower()
    )
"""
