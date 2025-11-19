# Temporarily disabled - projects and sessions integration
# This file will be re-enabled in the future
"""
from uuid import UUID

import pytest

from audiostack.projects.project import Project
from audiostack.tests.utils import create_test_project_name


@pytest.mark.integration
def test_project_create_and_get(test_project: Project.Item) -> None:
    # CREATE (already done by fixture)
    assert test_project.projectName is not None
    assert test_project.projectId is not None
    assert test_project.folderId is not None
    assert test_project.createdBy is not None
    assert test_project.createdAt is not None

    # READ
    retrieved = Project.get(projectId=UUID(test_project.projectId))
    assert retrieved.projectId == test_project.projectId
    assert retrieved.projectName == test_project.projectName
    assert retrieved.folderId == test_project.folderId
    assert retrieved.createdBy == test_project.createdBy
    assert retrieved.createdAt == test_project.createdAt


@pytest.mark.integration
def test_project_listing(test_project: Project.Item) -> None:
    \"\"\"Test project listing against real API.\"\"\"
    response = Project.list()

    assert isinstance(response.projects, list)
    assert hasattr(response, "projects")

    project_ids = [p.projectId for p in response.projects]
    assert test_project.projectId in project_ids

    test_project_found = next(
        (p for p in response.projects if p.projectId == test_project.projectId),
        None,
    )
    assert test_project_found is not None
    assert test_project_found.projectName == test_project.projectName


@pytest.mark.integration
def test_project_duplicate_name_handling() -> None:
    \"\"\"Test that duplicate project names are properly rejected.\"\"\"
    project_name = create_test_project_name()
    project1 = Project.create(projectName=project_name)
    # Attempt to create duplicate should fail
    with pytest.raises(Exception) as exc_info:
        Project.create(projectName=project_name)
    assert "already exists" in str(exc_info.value)

    retrieved = Project.get(projectId=UUID(project1.projectId))
    assert retrieved.projectId == project1.projectId


@pytest.mark.integration
def test_project_validation_errors() -> None:
    \"\"\"Test project creation validation against real API.\"\"\"
    with pytest.raises(Exception) as exc_info:
        Project.create(projectName="")
    error_str = str(exc_info.value).lower()
    assert any(
        keyword in error_str
        for keyword in [
            "422",
            "validation",
            "invalid",
            "field required",
            "missing",
        ]
    )


@pytest.mark.integration
def test_project_not_found_error() -> None:
    \"\"\"Test project retrieval with non-existent ID.\"\"\"
    with pytest.raises(Exception) as exc_info:
        Project.get(projectId=UUID("00000000-0000-0000-0000-000000000000"))
    error_str = str(exc_info.value).lower()
    assert "404" in str(exc_info.value) or "not found" in error_str


@pytest.mark.integration
def test_multiple_projects_workflow(
    multiple_test_projects: list[Project.Item],
) -> None:
    \"\"\"Test operations with multiple projects.\"\"\"
    assert len(multiple_test_projects) == 3

    all_projects = Project.list()
    project_ids = [p.projectId for p in all_projects.projects]

    for project in multiple_test_projects:
        assert project.projectId in project_ids

        retrieved = Project.get(projectId=UUID(project.projectId))
        assert retrieved.projectId == project.projectId
        assert retrieved.projectName == project.projectName
"""
