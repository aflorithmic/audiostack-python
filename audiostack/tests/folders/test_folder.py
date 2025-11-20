import os
import random
from uuid import UUID

import audiostack
from audiostack.folders.folder import Folder

audiostack.api_base = os.environ.get("AUDIO_STACK_DEV_URL", "https://v2.api.audio")
audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]  # type: ignore

test_constants: dict = {}


def create_test_folder_name() -> str:
    return f"test_folder_{random.randint(1000, 9999)}"


def test_create() -> None:
    r = Folder.create(name=create_test_folder_name())
    test_constants["folderId"] = r.folderId
    test_constants["folderName"] = r.folderName
    assert r.folderId is not None
    assert r.folderName is not None


def test_create_with_parent() -> None:
    parent_folder = Folder.create(name=create_test_folder_name())
    test_constants["parentFolderId"] = parent_folder.folderId

    r = Folder.create(
        name=create_test_folder_name(),
        parentFolderId=UUID(parent_folder.folderId),
    )
    test_constants["childFolderId"] = r.folderId
    assert r.folderId is not None
    assert r.parentFolderId == parent_folder.folderId



@pytest.mark.skip(reason="address in next pr")
def test_get() -> None:
    r = Folder.get(folderId=UUID(test_constants["folderId"]))
    # Folder.get() now returns ListResponse, get folder from currentPathChain
    assert len(r.currentPathChain) > 0, "Should have current path chain"
    folder = next(
        (f for f in r.currentPathChain if f.folderId == test_constants["folderId"]),
        None,
    )
    assert (
        folder is not None
    ), f"Folder {test_constants['folderId']} should be in currentPathChain"
    assert folder.folderId == test_constants["folderId"]


def test_get_with_pagination() -> None:
    """Test get() with pagination parameters."""
    r = Folder.get(folderId=UUID(test_constants["folderId"]), limit=10, offset=0)
    assert len(r.currentPathChain) > 0, "Should have current path chain"
    if r.pagination:
        assert r.pagination.get("limit") == 10
        assert r.pagination.get("offset") == 0


def test_list() -> None:
    root_list = Folder.list()
    assert isinstance(root_list.folders, list)
    assert isinstance(root_list.files, list)

    folder_list = Folder.list(path=test_constants["folderName"])
    assert isinstance(folder_list.folders, list)
    assert isinstance(folder_list.files, list)


def test_list_with_pagination() -> None:
    """Test list() with pagination parameters."""
    result = Folder.list(limit=10)
    assert isinstance(result.folders, list)
    assert isinstance(result.files, list)
    if result.pagination:
        assert result.pagination.get("limit") == 10

    result = Folder.list(offset=5)
    assert isinstance(result.folders, list)
    assert isinstance(result.files, list)
    if result.pagination:
        assert result.pagination.get("offset") == 5

    result = Folder.list(limit=20, offset=10)
    assert isinstance(result.folders, list)
    assert isinstance(result.files, list)
    if result.pagination:
        assert result.pagination.get("limit") == 20
        assert result.pagination.get("offset") == 10


def test_list_files() -> None:
    """Test list_files() method."""
    files = Folder.list_files(folderId=UUID(test_constants["folderId"]))
    assert isinstance(files, list)


def test_list_files_with_pagination() -> None:
    """Test list_files() with pagination parameters."""
    files = Folder.list_files(
        folderId=UUID(test_constants["folderId"]), limit=5, offset=0
    )
    assert isinstance(files, list)


def test_search() -> None:
    search_results = Folder.search(query=test_constants["folderName"])
    assert isinstance(search_results.folders, list)
    assert isinstance(search_results.files, list)


def test_patch() -> None:
    new_name = create_test_folder_name()
    patched_folder = Folder.patch(
        folderId=UUID(test_constants["folderId"]), folderName=new_name
    )
    test_constants["updatedFolderName"] = new_name
    assert patched_folder.folderName == new_name

    # Verify with get() - now returns ListResponse
    r = Folder.get(folderId=UUID(test_constants["folderId"]))
    assert len(r.currentPathChain) > 0, "Should have current path chain"
    folder = r.currentPathChain[-1]  # Last item is the current folder
    assert folder.folderName == new_name


def test_get_root_folder_id() -> None:
    root_id = Folder.get_root_folder_id()
    assert isinstance(root_id, str)
    assert len(root_id) > 0


def test_delete() -> None:
    if "childFolderId" in test_constants:
        result = Folder.delete(folderId=UUID(test_constants["childFolderId"]))
        assert isinstance(result, str)

    if "parentFolderId" in test_constants:
        result = Folder.delete(folderId=UUID(test_constants["parentFolderId"]))
        assert isinstance(result, str)

    result = Folder.delete(folderId=UUID(test_constants["folderId"]))
    assert isinstance(result, str)
