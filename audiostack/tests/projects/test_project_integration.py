"""
Integration tests for Projects endpoint against AudioStack API.
"""

import os
import random
from typing import Generator
from uuid import UUID

import pytest

import audiostack
from audiostack.projects.project import Project
from audiostack.tests.utils import create_test_project_name

audiostack.api_base = os.environ.get("AUDIO_STACK_DEV_URL", "https://v2.api.audio")
audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]  # type: ignore

# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture(scope="session")
def test_project() -> Generator[Project.Item, None, None]:
    """Session-scoped fixture that creates a project for all tests."""
    project_name = create_test_project_name()
    project = Project.create(projectName=project_name)
    yield project


@pytest.fixture
def multiple_test_projects() -> Generator[list[Project.Item], None, None]:
    """Create multiple test projects for integration testing."""
    projects = []
    for i in range(3):
        project_name = f"test_project_multi_{i}_{random.randint(1000, 9999)}"
        project = Project.create(projectName=project_name)
        projects.append(project)
    yield projects


# ============================================================================
# INTEGRATION TESTS
# ============================================================================


@pytest.mark.integration
def test_project_crud_workflow(test_project: Project.Item) -> None:
    """Test complete CRUD workflow against real API."""
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
    """Test project listing against real API."""
    response = Project.list()

    assert isinstance(response.projects, list)
    assert hasattr(response, "projects")

    project_ids = [p.projectId for p in response.projects]
    assert test_project.projectId in project_ids

    # Find our test project in the list
    test_project_found = next(
        (p for p in response.projects if p.projectId == test_project.projectId), None
    )
    assert test_project_found is not None
    assert test_project_found.projectName == test_project.projectName


@pytest.mark.integration
def test_project_duplicate_name_handling() -> None:
    """Test that duplicate project names are properly rejected."""
    project_name = create_test_project_name()
    project1 = Project.create(projectName=project_name)

    # Attempt to create duplicate should fail
    with pytest.raises(Exception) as exc_info:
        Project.create(projectName=project_name)
    assert "already exists" in str(exc_info.value)

    # Verify first project still exists
    retrieved = Project.get(projectId=UUID(project1.projectId))
    assert retrieved.projectId == project1.projectId


@pytest.mark.integration
def test_project_validation_errors() -> None:
    """Test project creation validation against real API."""
    # Test empty name
    with pytest.raises(Exception) as exc_info:
        Project.create(projectName="")
    error_str = str(exc_info.value).lower()
    assert any(
        keyword in error_str
        for keyword in ["422", "validation", "invalid", "field required", "missing"]
    )


@pytest.mark.integration
def test_project_not_found_error() -> None:
    """Test project retrieval with non-existent ID."""
    with pytest.raises(Exception) as exc_info:
        Project.get(projectId=UUID("00000000-0000-0000-0000-000000000000"))
    error_str = str(exc_info.value).lower()
    assert "404" in str(exc_info.value) or "not found" in error_str


@pytest.mark.integration
def test_multiple_projects_workflow(multiple_test_projects: list[Project.Item]) -> None:
    """Test operations with multiple projects."""
    # Verify all projects were created
    assert len(multiple_test_projects) == 3

    # Test listing includes all our projects
    all_projects = Project.list()
    project_ids = [p.projectId for p in all_projects.projects]

    for project in multiple_test_projects:
        assert project.projectId in project_ids

        # Verify each project can be retrieved individually
        retrieved = Project.get(projectId=UUID(project.projectId))
        assert retrieved.projectId == project.projectId
        assert retrieved.projectName == project.projectName
