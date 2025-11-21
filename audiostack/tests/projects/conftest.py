# Temporarily disabled - projects and sessions integration
# This file will be re-enabled in the future
"""
import os
import random
from typing import Generator

import pytest

import audiostack
from audiostack.projects.project import Project
from audiostack.tests.utils import create_test_project_name

audiostack.api_base = os.environ.get(
    "AUDIO_STACK_DEV_URL", "https://v2.api.audio"
)
audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]  # type: ignore


@pytest.fixture(scope="session")
def test_project() -> Generator[Project.Item, None, None]:
    \"\"\"Session-scoped fixture that creates a project for all tests.\"\"\"
    project_name = create_test_project_name()
    project = Project.create(projectName=project_name)
    yield project


@pytest.fixture
def multiple_test_projects() -> Generator[list[Project.Item], None, None]:
    \"\"\"Create multiple test projects for integration testing.\"\"\"
    projects = []
    for i in range(3):
        project_name = f"test_project_multi_{i}_{random.randint(1000, 9999)}"
        project = Project.create(projectName=project_name)
        projects.append(project)
    yield projects
"""
