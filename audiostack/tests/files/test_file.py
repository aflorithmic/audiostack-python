import os
from uuid import UUID

import audiostack
from audiostack.files.file import File

audiostack.api_base = os.environ.get("AUDIO_STACK_DEV_URL", "https://v2.api.audio")
audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]  # type: ignore

test_constants = {}


def test_create() -> None:
    """Test file creation with new signature."""
    r = File.create(
        localPath="example.mp3", uploadPath="test.mp3", fileName="test_file.mp3"
    )
    test_constants["fileId"] = r.fileId
    test_constants["fileName"] = r.fileName
    test_constants["folderId"] = r.folderId
    print(f"Created file: {r.fileName} with ID: {r.fileId}")


def test_get() -> None:
    """Test file retrieval."""
    r = File.get(fileId=test_constants["fileId"])
    print(f"Retrieved file: {r.fileName}")
    assert r.fileId == test_constants["fileId"]


def test_get_file_categories() -> None:
    """Test getting file categories and types."""
    categories = File.get_file_categories()
    print(f"File categories: {categories}")
    assert "fileTypes" in categories


def test_patch() -> None:
    """Test file patching/updating."""
    r = File.patch(fileId=test_constants["fileId"], file_name="updated_test_file.mp3")
    print(f"Patched file: {r.fileName}")
    assert r.fileName == "updated_test_file.mp3"


# def test_copy() -> None:
#     """Test file copying to another folder."""
#     from audiostack.folders.folder import Folder

#     folder = Folder.create(name="test_copy_folder")
#     test_constants["copyFolderId"] = folder.folderId

#     r = File.copy(
#         fileId=test_constants["fileId"],
#         currentFolderId=UUID(test_constants["folderId"]),
#         newFolderId=UUID(folder.folderId),
#     )
#     print(f"Copied file: {r.fileName} to folder: {folder.folderName}")
#     assert r.fileName == test_constants["fileName"]


def test_download() -> None:
    """Test file download (if URL is available)."""
    r = File.get(fileId=test_constants["fileId"])
    if r.url:
        r.download(fileName="downloaded_test.mp3", path="./")
        print("File downloaded successfully")
    else:
        print("File not yet processed, no URL available")


def test_delete() -> None:
    """Test file deletion."""
    File.delete(fileId=test_constants["fileId"])
    print(f"Deleted file: {test_constants['fileId']}")


def test_delete_copy() -> None:
    """Test deleting the copied file."""
    if "copyFolderId" in test_constants:
        # This would need to be implemented based on how you want to
        # handle deleting files from specific folders
        print("Copy file deletion test - implementation depends on requirements")
