import os
from uuid import UUID

import pytest

import audiostack
from audiostack.folders.folder import Folder
from audiostack.tests.utils import create_test_folder_name

audiostack.api_base = os.environ.get("AUDIO_STACK_DEV_URL", "https://v2.api.audio")
audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]  # type: ignore


def test_create(cleanup_resources: dict) -> None:
    """Test folder creation."""
    folder = Folder.create(name=create_test_folder_name())
    cleanup_resources["folder_ids"].append(folder.folderId)

    assert folder.folderId is not None
    assert folder.folderName is not None


def test_create_with_parent(cleanup_resources: dict) -> None:
    """Test folder creation with parent folder."""
    parent_folder = Folder.create(name=create_test_folder_name())
    cleanup_resources["folder_ids"].append(parent_folder.folderId)

    assert parent_folder.folderId is not None
    parent_verification = Folder.get(folderId=UUID(parent_folder.folderId))
    assert len(parent_verification.currentPathChain) > 0

    child_folder = Folder.create(
        name=create_test_folder_name(),
        parentFolderId=UUID(parent_folder.folderId),
    )
    cleanup_resources["folder_ids"].append(child_folder.folderId)

    assert child_folder.folderId is not None
    assert child_folder.parentFolderId == parent_folder.folderId


def test_get(test_folder: Folder.Item) -> None:
    response = Folder.get(folderId=UUID(test_folder.folderId))
    # Folder.get() now returns ListResponse, get folder from currentPathChain
    assert len(response.currentPathChain) > 0, "Should have current path chain"
    folder = next(
        (f for f in response.currentPathChain if f.folderId == test_folder.folderId),
        None,
    )
    assert (
        folder is not None
    ), f"Folder {test_folder.folderId} should be in currentPathChain"
    assert folder.folderId == test_folder.folderId


def test_list_root() -> None:
    root_list = Folder.list()
    assert isinstance(root_list.folders, list)
    assert isinstance(root_list.files, list)


def test_list_by_path(test_folder: Folder.Item) -> None:
    folder_list = Folder.list(path=test_folder.folderName)
    assert isinstance(folder_list.folders, list)
    assert isinstance(folder_list.files, list)


def test_list_files(test_folder: Folder.Item) -> None:
    result = Folder.list_files(folderId=UUID(test_folder.folderId))
    assert isinstance(result.files, list)
    assert hasattr(result, "pagination")


def test_list_files_with_pagination(test_folder: Folder.Item) -> None:
    result = Folder.list_files(folderId=UUID(test_folder.folderId), limit=5, offset=0)
    assert isinstance(result.files, list)
    if result.pagination:
        assert result.pagination.get("limit") == 5
        assert result.pagination.get("offset") == 0


def test_patch(test_folder: Folder.Item) -> None:
    new_name = create_test_folder_name()
    patched_folder = Folder.patch(
        folderId=UUID(test_folder.folderId), folderName=new_name
    )
    assert patched_folder.folderName == new_name

    # Verify with get() - now returns ListResponse
    response = Folder.get(folderId=UUID(test_folder.folderId))
    assert len(response.currentPathChain) > 0, "Should have current path chain"
    # Find the folder in the path chain that matches our folderId
    folder = next(
        (f for f in response.currentPathChain if f.folderId == test_folder.folderId),
        None,
    )
    assert folder is not None, f"Folder {test_folder.folderId} should be in path chain"
    assert folder.folderName == new_name


def test_get_root_folder_id() -> None:
    root_id = Folder.get_root_folder_id()
    assert isinstance(root_id, str)
    assert len(root_id) > 0


def test_delete() -> None:
    folder = Folder.create(name=create_test_folder_name())

    result = Folder.delete(folderId=UUID(folder.folderId))
    assert isinstance(result, str)

    with pytest.raises(Exception):
        Folder.get(folderId=UUID(folder.folderId))
