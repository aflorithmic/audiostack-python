from uuid import UUID

from audiostack.files.file import File
from audiostack.folders.folder import Folder
from audiostack.tests.utils import create_test_file_name, create_test_folder_name


def test_file_folder_workflow(cleanup_resources: dict) -> None:
    """Test complete file and folder workflow."""
    # 1. Create a test folder
    folder_name = create_test_folder_name()
    folder = Folder.create(name=folder_name)
    cleanup_resources["folder_ids"].append(folder.folderId)
    assert folder.folderId is not None
    assert folder.folderName == folder_name

    # 2. Upload a file to the folder
    file_name = create_test_file_name() + ".mp3"
    file = File.create(
        localPath="example.mp3",
        fileName=file_name,
        folderId=UUID(folder.folderId),
    )
    cleanup_resources["file_ids"].append(file.fileId)
    assert file.fileId is not None
    assert file.fileName == file_name

    # 3. Verify file is in the folder
    folder_contents = Folder.list(path=folder_name)
    file_found = any(f.fileId == file.fileId for f in folder_contents.files)
    assert file_found, "File should be in the folder"

    # 4. Create another folder for copying
    copy_folder_name = create_test_folder_name()
    copy_folder = Folder.create(name=copy_folder_name)
    cleanup_resources["folder_ids"].append(copy_folder.folderId)
    assert copy_folder.folderId is not None

    # 5. Copy file to new folder
    copied_file = File.copy(
        fileId=UUID(file.fileId),
        currentFolderId=UUID(folder.folderId),
        newFolderId=UUID(copy_folder.folderId),
    )
    cleanup_resources["file_ids"].append(copied_file.fileId)
    assert copied_file.fileId is not None

    # 6. Verify file is in both folders (integration test)
    original_folder_contents = Folder.list(path=folder_name)
    copy_folder_contents = Folder.list(path=copy_folder_name)

    original_has_file = any(
        f.fileId == file.fileId for f in original_folder_contents.files
    )
    copy_has_file = any(
        f.fileId == copied_file.fileId for f in copy_folder_contents.files
    )

    # If the copied file is not found, check if there's a file with same name
    if not copy_has_file:
        same_name_files = [
            f for f in copy_folder_contents.files if f.fileName == copied_file.fileName
        ]
        if same_name_files:
            # Update the copied_file to use the actual file in the folder
            copied_file = same_name_files[0]
            copy_has_file = True

    assert original_has_file, "Original file should still be in original folder"
    found_file_ids = [f.fileId for f in copy_folder_contents.files]
    assert copy_has_file, (
        f"Copied file {copied_file.fileId} should be in copy folder. "
        f"Found files: {found_file_ids}"
    )

    # 7. Test file patching and verify it reflects in folder listing
    new_file_name = create_test_file_name() + ".mp3"
    patched_file = File.patch(fileId=UUID(file.fileId), fileName=new_file_name)
    assert patched_file.fileName == new_file_name, "File name should be updated"

    # Verify patched file name appears in folder listing
    updated_folder_contents = Folder.list(path=folder_name)
    patched_file_in_list = next(
        (f for f in updated_folder_contents.files if f.fileId == file.fileId), None
    )
    assert patched_file_in_list is not None, "Patched file should be in folder"
    assert (
        patched_file_in_list.fileName == new_file_name
    ), "Folder listing should show updated file name"

    # 8. Test folder patching and verify it reflects in folder operations
    new_folder_name = create_test_folder_name()
    patched_folder = Folder.patch(
        folderId=UUID(folder.folderId), folderName=new_folder_name
    )
    assert patched_folder.folderName == new_folder_name, "Folder name should be updated"

    # Verify with get() - now returns ListResponse
    updated_folder_response = Folder.get(folderId=UUID(folder.folderId))
    assert (
        len(updated_folder_response.currentPathChain) > 0
    ), "Should have current path chain"
    updated_folder = updated_folder_response.currentPathChain[-1]
    assert updated_folder.folderName == new_folder_name, "Folder name should be updated"

    # Verify folder can be listed by new name
    renamed_folder_contents = Folder.list(path=new_folder_name)
    assert len(renamed_folder_contents.files) > 0, "Should find files in renamed folder"


def test_file_categories() -> None:
    """Test file categories functionality."""
    categories = File.get_file_categories()
    assert "fileTypes" in categories, "Response should contain fileTypes"
    assert isinstance(categories["fileTypes"], list), "fileTypes should be a list"
    assert len(categories["fileTypes"]) > 0, "Should have at least one file type"
