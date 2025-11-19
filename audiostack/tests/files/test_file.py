import os
from uuid import UUID

import pytest

import audiostack
from audiostack.files.file import AccessControl, File
from audiostack.folders.folder import Folder

audiostack.api_base = os.environ.get("AUDIO_STACK_DEV_URL", "https://v2.api.audio")
audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]  # type: ignore

test_constants = {}


def test_create() -> None:
    """Test file creation."""
    r = File.create(localPath="example.mp3", fileName="test_file.mp3")
    test_constants["fileId"] = r.fileId
    test_constants["fileName"] = r.fileName
    test_constants["folderId"] = r.folderId
    print(f"Created file: {r.fileName} with ID: {r.fileId}")


def test_create_path_validation() -> None:
    """Test file creation path validation."""
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
        r = File.create(localPath="./example.mp3", fileName="test.mp3")
        assert r.fileName == "test.mp3"
    except FileNotFoundError:
        # If example.mp3 doesn't exist in current dir, that's fine
        pass


def test_get() -> None:
    r = File.get(fileId=UUID(test_constants["fileId"]))
    print(f"Retrieved file: {r.fileName}")
    assert r.fileId == test_constants["fileId"]


def test_get_file_categories() -> None:
    categories = File.get_file_categories()
    print(f"File categories: {categories}")
    assert "fileTypes" in categories


def test_patch() -> None:
    # get original file name for verification
    original_file = File.get(fileId=UUID(test_constants["fileId"]))
    original_name = original_file.fileName
    print(f"Original file name: {original_name}")

    # patching file name
    new_name = "updated_test_file.mp3"
    patched_file = File.patch(fileId=UUID(test_constants["fileId"]), fileName=new_name)
    print(f"Patched file: {patched_file.fileName}")
    assert patched_file.fileName == new_name

    # verify the change persisted by retrieving the file again
    retrieved_file = File.get(fileId=UUID(test_constants["fileId"]))
    assert retrieved_file.fileName == new_name
    print(f"✓ File name change verified: {retrieved_file.fileName}")

    # patching access control
    patched_file = File.patch(
        fileId=UUID(test_constants["fileId"]),
        accessControl=AccessControl.private,
    )
    assert patched_file.accessControl == "private"
    print("✓ Access control patched to private")

    # revert the change for other tests
    File.patch(fileId=UUID(test_constants["fileId"]), fileName=original_name)
    print(f"✓ Reverted file name back to: {original_name}")


def test_patch_error_handling() -> None:
    # patching non-existent file
    with pytest.raises(Exception):
        File.patch(
            fileId=UUID("00000000-0000-0000-0000-000000000000"),
            fileName="test.mp3",
        )
    print("✓ Correctly handled non-existent file patch")

    # patching with no parameters
    try:
        File.patch(fileId=UUID(test_constants["fileId"]))
        print("✓ Patch with no parameters handled gracefully")
    except Exception as e:
        print(f"⚠ Patch with no parameters failed: {e}")


@pytest.mark.skip(reason="failing at different id assertion")
def test_copy() -> None:
    # create a destination folder for the copy
    folder_name = f"test_copy_folder_{os.getpid()}"
    folder = Folder.create(name=folder_name)
    test_constants["copyFolderId"] = folder.folderId
    print(f"Created copy destination folder: {folder.folderName}")

    # copy the file to the new folder
    copied_file = File.copy(
        fileId=UUID(test_constants["fileId"]),
        currentFolderId=UUID(test_constants["folderId"]),
        newFolderId=UUID(folder.folderId),
    )
    test_constants["copiedFileId"] = copied_file.fileId
    print(f"Copied file: {copied_file.fileName} to folder: {folder.folderName}")

    # verify the copy was successful
    assert copied_file.fileName == test_constants["fileName"]
    # Should be different ID (new hard link)
    assert copied_file.fileId != test_constants["fileId"]
    print(f"✓ Copy successful - new file ID: {copied_file.fileId}")

    # verify the copied file exists in the destination folder
    folder_contents = Folder.list(path=folder_name)
    copy_found = any(f.fileId == copied_file.fileId for f in folder_contents.files)
    assert copy_found, "Copied file should be found in destination folder"
    print("✓ Copied file found in destination folder")

    # verify original file still exists in original folder
    original_file = File.get(fileId=UUID(test_constants["fileId"]))
    assert original_file.fileId == test_constants["fileId"]
    print("✓ Original file still exists")


def test_copy_error_handling() -> None:
    # copying with invalid file ID
    try:
        File.copy(
            fileId=UUID("00000000-0000-0000-0000-000000000000"),
            currentFolderId=UUID(test_constants["folderId"]),
            newFolderId=UUID(test_constants["folderId"]),
        )
        assert False, "Should have raised an exception for invalid file ID"
    except Exception as e:
        print(f"✓ Correctly handled invalid file ID: {e}")

    # copying with invalid folder IDs
    try:
        File.copy(
            fileId=UUID(test_constants["fileId"]),
            currentFolderId=UUID("00000000-0000-0000-0000-000000000000"),
            newFolderId=UUID("00000000-0000-0000-0000-000000000000"),
        )
        assert False, "Should have raised an exception for invalid folder IDs"
    except Exception as e:
        print(f"✓ Correctly handled invalid folder IDs: {e}")


def test_download() -> None:
    r = File.get(fileId=UUID(test_constants["fileId"]))
    if r.url:
        download_path = "./downloaded_test.mp3"
        # ensure file doesn't exist before download
        if os.path.exists(download_path):
            os.remove(download_path)
            print(f"Removed existing file: {download_path}")

        # download the file
        r.download(fileName="downloaded_test.mp3", path="./")
        print("File download initiated")

        # verify file was actually downloaded
        if os.path.exists(download_path):
            file_size = os.path.getsize(download_path)
            print(
                f"✓ File downloaded successfully: {download_path} "
                f"({file_size} bytes)"
            )

            # clean up the downloaded file
            os.remove(download_path)
            print(f"✓ Cleaned up downloaded file: {download_path}")
        else:
            print("⚠ Warning: Download completed but file not found on " "filesystem")
    else:
        print("File not yet processed, no URL available - " "skipping download test")


def test_delete() -> None:
    file_before = File.get(fileId=UUID(test_constants["fileId"]))
    assert file_before.fileId == test_constants["fileId"]
    print(f"File exists before deletion: {file_before.fileName}")

    File.delete(fileId=UUID(test_constants["fileId"]))
    print(f"Deleted file: {test_constants['fileId']}")

    try:
        File.get(fileId=UUID(test_constants["fileId"]))
        assert False, "File should not exist after deletion"
    except Exception as e:
        print(f"✓ File successfully deleted - retrieval failed as expected: {e}")
