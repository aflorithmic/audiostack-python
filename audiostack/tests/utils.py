"""
Shared test utilities for AudioStack SDK tests.

This module provides common helper functions used across multiple test suites
to avoid code duplication and ensure consistency.
"""

import random
from typing import Optional


def create_test_name(prefix: str = "test", suffix: Optional[str] = None) -> str:
    """Generate a unique test name with optional prefix and suffix.

    Args:
        prefix: Prefix for the test name (default: "test")
        suffix: Optional suffix to append (default: random number)

    Returns:
        str: A unique test name

    Examples:
        >>> create_test_name("project")
        "test_project_1234"
        >>> create_test_name("session", "audio")
        "test_session_audio_5678"
    """
    if suffix:
        return f"test_{prefix}_{suffix}_{random.randint(1000, 9999)}"
    return f"test_{prefix}_{random.randint(1000, 9999)}"


def create_test_project_name() -> str:
    """Generate a unique test project name.

    Returns:
        str: A unique project name for testing
    """
    return create_test_name("project")


def create_test_session_name() -> str:
    """Generate a unique test session name.

    Returns:
        str: A unique session name for testing
    """
    return create_test_name("session")


def create_test_folder_name() -> str:
    """Generate a unique test folder name.

    Returns:
        str: A unique folder name for testing
    """
    return create_test_name("folder")


def create_test_file_name() -> str:
    """Generate a unique test file name.

    Returns:
        str: A unique file name for testing
    """
    return create_test_name("file")


def create_test_script_name() -> str:
    """Generate a unique test script name.

    Returns:
        str: A unique script name for testing
    """
    return create_test_name("script")
