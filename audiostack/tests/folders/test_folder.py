# TODO: User proper pytest fixtures
import os
import random
from uuid import UUID

import pytest

import audiostack
from audiostack.folders.folder import Folder

audiostack.api_base = os.environ.get("AUDIO_STACK_DEV_URL", "https://v2.api.audio")
audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]  # type: ignore

test_constants: dict = {}


def create_test_folder_name() -> str:
    return f"test_folder_{random.randint(1000, 9999)}"


def test_create() -> None:
    """Test folder creation."""
    r = Folder.create(name=create_test_folder_name())
    test_constants["folderId"] = r.folderId
    test_constants["folderName"] = r.folderName
    print(f"Created folder: {r.folderName} with ID: {r.folderId}")


def test_create_with_parent() -> None:
    """Test folder creation with parent folder."""
    parent_folder = Folder.create(name=create_test_folder_name())
    test_constants["parentFolderId"] = parent_folder.folderId

    r = Folder.create(
        name=create_test_folder_name(), parentFolderId=UUID(parent_folder.folderId)
    )
    test_constants["childFolderId"] = r.folderId
    print(f"Created child folder: {r.folderName} under: " f"{parent_folder.folderName}")

@pytest.mark.skip(reason="address in next pr")
def test_get() -> None:
    """Test folder retrieval."""
    r = Folder.get(folderId=UUID(test_constants["folderId"]))
    print(f"Retrieved folder: {r.folderName}")
    assert r.folderId == test_constants["folderId"]

@pytest.mark.skip(reason="address in next pr")
def test_list() -> None:
    """Test listing folders and files."""
    root_list = Folder.list()
    print(
        f"Root folder contains {len(root_list.folders)} folders and "
        f"{len(root_list.files)} files"
    )
    assert isinstance(root_list.folders, list)
    assert isinstance(root_list.files, list)

    folder_list = Folder.list(path=test_constants["folderName"])
    print(
        f"Folder {test_constants['folderName']} contains "
        f"{len(folder_list.folders)} folders and "
        f"{len(folder_list.files)} files"
    )


def test_search() -> None:
    """Test folder and file search."""
    search_results = Folder.search(query=test_constants["folderName"])
    print(
        f"Search for '{test_constants['folderName']}' found "
        f"{len(search_results.folders)} folders and "
        f"{len(search_results.files)} files"
    )
    assert isinstance(search_results.folders, list)
    assert isinstance(search_results.files, list)


@pytest.mark.skip(reason="address in next pr")
def test_patch() -> None:
    """Test folder name modification."""
    new_name = create_test_folder_name()
    Folder.patch(folderId=UUID(test_constants["folderId"]), folderName=new_name)
    test_constants["updatedFolderName"] = new_name
    print(f"Updated folder name to: {new_name}")

    r = Folder.get(folderId=UUID(test_constants["folderId"]))
    assert r.folderName == new_name


@pytest.mark.skip(reason="address in next pr")
def test_get_root_folder_id() -> None:
    """Test getting root folder ID."""
    root_id = Folder.get_root_folder_id()
    print(f"Root folder ID: {root_id}")
    assert isinstance(root_id, str)
    assert len(root_id) > 0


def test_delete() -> None:
    """Test folder deletion."""
    if "childFolderId" in test_constants:
        Folder.delete(folderId=UUID(test_constants["childFolderId"]))
        print(f"Deleted child folder: {test_constants['childFolderId']}")

    if "parentFolderId" in test_constants:
        Folder.delete(folderId=UUID(test_constants["parentFolderId"]))
        print(f"Deleted parent folder: {test_constants['parentFolderId']}")

    Folder.delete(folderId=UUID(test_constants["folderId"]))
    print(f"Deleted folder: {test_constants['folderId']}")
