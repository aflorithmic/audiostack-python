import os
from uuid import UUID

import pytest

import audiostack
from audiostack.files.file import AccessControl, File
from audiostack.folders.folder import Folder
from audiostack.tests.utils import create_test_file_name

audiostack.api_base = os.environ.get("AUDIO_STACK_DEV_URL", "https://v2.api.audio")
audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]  # type: ignore


def test_create(cleanup_resources: dict) -> None:
    root_folder_id = Folder.get_root_folder_id()
    file = File.create(
        localPath="example.mp3",
        fileName=create_test_file_name() + ".mp3",
        folderId=UUID(root_folder_id),
    )
    cleanup_resources["file_ids"].append(file.fileId)

    assert file.fileId is not None
    assert file.fileName is not None
    assert file.folderId is not None


def test_create_path_validation(cleanup_resources: dict) -> None:
    # empty path
    with pytest.raises(ValueError, match="Please supply a file path"):
        File.create(localPath="", fileName="test.mp3")

    # non-existent file
    with pytest.raises(FileNotFoundError):
        File.create(localPath="nonexistent_file.mp3", fileName="test.mp3")

    # directory instead of file
    with pytest.raises(ValueError, match="directory, not a file"):
        File.create(localPath=".", fileName="test.mp3")

    try:
        unique_name = create_test_file_name() + ".mp3"
        file = File.create(localPath="./example.mp3", fileName=unique_name)
        cleanup_resources["file_ids"].append(file.fileId)
        assert file.fileName == unique_name
    except FileNotFoundError as e:
        print(e)
        pass


def test_get(test_file: File.Item) -> None:
    retrieved_file = File.get(fileId=UUID(test_file.fileId))
    assert retrieved_file.fileId == test_file.fileId
    assert retrieved_file.fileName is not None


def test_get_file_categories() -> None:
    categories = File.get_file_categories()
    assert "fileTypes" in categories
    assert isinstance(categories, dict)


def test_patch_file_name(test_file: File.Item) -> None:
    new_name = create_test_file_name() + ".mp3"
    patched_file = File.patch(fileId=UUID(test_file.fileId), fileName=new_name)
    assert patched_file.fileName == new_name

    # verify the change persisted by retrieving the file again
    retrieved_file = File.get(fileId=UUID(test_file.fileId))
    assert retrieved_file.fileName == new_name


def test_patch_access_control(test_file: File.Item) -> None:
    patched_file = File.patch(
        fileId=UUID(test_file.fileId),
        accessControl=AccessControl.private,
    )
    assert patched_file.accessControl == "private"

    # verify access control change persisted
    retrieved_file = File.get(fileId=UUID(test_file.fileId))
    assert retrieved_file.accessControl == "private"


def test_patch_no_parameters(test_file: File.Item) -> None:
    result = File.patch(fileId=UUID(test_file.fileId))
    assert result is not None


def test_patch_error_handling() -> None:
    # patching non-existent file
    with pytest.raises(Exception):
        File.patch(
            fileId=UUID("00000000-0000-0000-0000-000000000000"),
            fileName="test.mp3",
        )


def test_copy_returns_new_file_item(
    test_file: File.Item, cleanup_resources: dict
) -> None:
    # create a destination folder for the copy
    folder = Folder.create(name=create_test_file_name())
    cleanup_resources["folder_ids"].append(folder.folderId)

    # copy the file to the new folder
    copied_file = File.copy(
        fileId=UUID(test_file.fileId),
        currentFolderId=UUID(test_file.folderId),
        newFolderId=UUID(folder.folderId),
    )
    cleanup_resources["file_ids"].append(copied_file.fileId)

    # verify the copy operation returns expected results
    assert copied_file.fileName == test_file.fileName
    # should be different ID (new hard link)
    assert copied_file.fileId != test_file.fileId
    assert copied_file.fileId is not None
    assert copied_file.folderId == folder.folderId

    # verify original file still exists
    original_file = File.get(fileId=UUID(test_file.fileId))
    assert original_file.fileId == test_file.fileId


def test_copy_error_handling(test_file: File.Item) -> None:
    # copying with invalid file ID
    with pytest.raises(Exception):
        File.copy(
            fileId=UUID("00000000-0000-0000-0000-000000000000"),
            currentFolderId=UUID(test_file.folderId),
            newFolderId=UUID(test_file.folderId),
        )

    # copying with invalid folder IDs
    with pytest.raises(Exception):
        File.copy(
            fileId=UUID(test_file.fileId),
            currentFolderId=UUID("00000000-0000-0000-0000-000000000000"),
            newFolderId=UUID("00000000-0000-0000-0000-000000000000"),
        )


def test_download(test_file: File.Item) -> None:
    file = File.get(fileId=UUID(test_file.fileId))
    if file.url:
        download_path = "./downloaded_test.mp3"
        # ensure file doesn't exist before download
        if os.path.exists(download_path):
            os.remove(download_path)

        # download the file
        file.download(fileName="downloaded_test.mp3", path="./")

        # verify file was actually downloaded
        assert os.path.exists(
            download_path
        ), "Downloaded file should exist on filesystem"
        file_size = os.path.getsize(download_path)
        assert file_size > 0, "Downloaded file should have content"

        # clean up the downloaded file
        os.remove(download_path)
        assert not os.path.exists(download_path), "Downloaded file should be removed"


def test_delete() -> None:
    # create a file to delete
    root_folder_id = Folder.get_root_folder_id()
    file = File.create(
        localPath="example.mp3",
        fileName=create_test_file_name() + ".mp3",
        folderId=UUID(root_folder_id),
    )

    file_before = File.get(fileId=UUID(file.fileId))
    assert file_before.fileId == file.fileId
    assert file_before.fileName is not None

    File.delete(fileId=UUID(file.fileId))

    # verify file no longer exists
    with pytest.raises(Exception):
        File.get(fileId=UUID(file.fileId))
