# Change Log
All notable changes to `audiostack` will be documented in this file.
 
The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [4.0.0] - 2025-01-XX

### New Features

#### Audioform API Integration
- **New Audioform class** with comprehensive audioform build management:
  - `Audioform.create(audioform)` - Create new audioform build requests
  - `Audioform.get(audioform_id, version, wait, timeoutThreshold)` - Retrieve audioform build status and results
  - `Audioform.Item` class with properties:
    - `audioform_id`: Unique audioform identifier
    - `status_code`: Build status code
    - `audioform`: Original audioform configuration
    - `result`: Build result with processed assets and metadata
- **Version support** for both "1" and "0.0.1" audioform formats
- **Automatic version handling** - version parameter automatically added to header

#### Brief API Integration
- **New Brief class** for AI-powered ad generation:
  - `Brief.create(brief, file_id, num_ads, audioform_version)` - Generate multiple ads from brief
  - `Brief.Item` class with properties:
    - `status_code`: Generation status code
    - `audioform_id`: Generated audioform identifier
    - `audioforms`: Array of audioforms
- **Flexible input options** - accept either brief configuration object or uploaded file ID
- **Configurable ad generation** - specify number of ads to generate (1-5, default 3)

#### Files and Folders API v2 Integration
- **Complete Files and Folders API overhaul** with new v2 endpoints:
  - **New API endpoints**: `/files` and `/folders` replacing legacy `/v3/file` and `/v3/folder`
  - **Enhanced file operations** with new methods:
    - `File.copy(fileId, currentFolderId, newFolderId)` - Copy files between folders
    - `File.patch(fileId, file_name, category_id, category_name)` - Update file metadata
    - `File.get_file_categories()` - Retrieve available file categories and types
    - `File.create(localPath, uploadPath, fileName, folderId, categoryId)` - Create files with required fileName parameter
  - **Enhanced folder operations** with new methods:
    - `Folder.create(name, parentFolderId)` - Create new folders
    - `Folder.get(folderId)` - Retrieve folder by ID
    - `Folder.delete(folderId)` - Delete folders
    - `Folder.list(path)` - List files and folders in directory (path optional)
    - `Folder.search(query)` - Search for files and folders
    - `Folder.patch(folderId, folderName)` - Update folder names
    - `Folder.get_root_folder_id()` - Get root folder ID
- **Updated response structures** with new field mappings:
  - `file_id` → `fileId` (UUID to string conversion)
  - `folder_id` → `folderId` (UUID to string conversion)
  - `parent_folder_id` → `parentFolderId` (optional field)
  - `file_category` → `fileCategory` (now dict instead of string)
  - `current_path_chain` → `currentPathChain` (list of Folder.Item objects)
- **New response classes**:
  - `Folder.ListResponse` - Contains folders, files, and currentPathChain
  - `Folder.SearchResponse` - Contains folders and files from search operations
- **Simplified file deletion** - `File.delete(fileId)` no longer requires `folderId`
- **Enhanced type safety** with proper UUID handling and optional field management

#### Projects and Sessions API Integration
- **New Project class** for project management:
  - `Project.create(projectName)` - Create new projects
  - `Project.get(projectId)` - Retrieve project by ID
  - `Project.list()` - List all projects
  - `Project.Item` class with properties:
    - `projectId`: Unique project identifier
    - `projectName`: Name of the project
    - `folderId`: Associated folder ID
    - `createdBy`: ID of user who created the project
    - `createdAt`: Creation timestamp
    - `lastModified`: Last modification timestamp (optional)

- **New Session class** for session management:
  - `Session.create(projectId, workflowId, sessionName, status, state, audioformId)` - Create new sessions
  - `Session.get(projectId, sessionId)` - Retrieve session by ID
  - `Session.list(projectId, workflowId)` - List sessions for a project with optional workflow filtering
  - `Session.update(projectId, sessionId, sessionName, status, state, audioformId)` - Update session metadata
  - `Session.delete(projectId, sessionId)` - Delete sessions
  - `Session.Item` class with properties:
    - `sessionId`: Unique session identifier
    - `sessionName`: Name of the session
    - `status`: Session status
    - `workflowId`: Associated workflow ID
    - `projectId`: Parent project ID
    - `createdBy`: ID of user who created the session
    - `createdAt`: Creation timestamp
    - `state`: Session state data (dict)
    - `lastModifiedBy`: ID of user who last modified the session (optional)
    - `lastModified`: Last modification timestamp (optional)
    - `audioformId`: Associated audioform ID (optional)

### API Changes

#### Python Version Requirement
- **BREAKING CHANGE**: Minimum Python version updated from 3.8 to 3.10
- **Rationale**: Python 3.8 and 3.9 reached End of Life (EOL)
- **Migration**: Users must upgrade to Python 3.10 or higher

### 📝 Migration Guide

#### For Python Version Upgrade
```bash
# Update Python version requirement
python --version  # Must be 3.10.0 or higher

# Update dependencies
pip install --upgrade audiostack
```

#### For Audioform Integration
```python
# Create audioform with v1 format
audioform_config = {
    "assets": {
        "script_0": {
            "type": "tts",
            "voiceRef": "voice_0",
            "text": "Sample text"
        }
    },
    "production": {"masteringPreset": "balanced"},
    "delivery": {"encoderPreset": "mp3"}
}

# Create audioform
audioform = Audioform.create(audioform_config)

# Get build status
result = Audioform.get(audioform.audioform_id, version="1")
```

#### For Brief Integration
```python
# Create brief from configuration
brief = {
    "script": {
        "productName": "Test Product",
        "productDescription": "A great product",
        "adLength": 30
    },
    "voices": [{"speed": None}],
    "production": {"masteringPreset": "balanced"},
    "delivery": {"encoderPreset": "mp3"}
}

# Generate ads
ads = Brief.create(brief=brief, num_ads=3, audioform_version="1")
```

#### For Files and Folders API v2 Integration

```python
# Create a folder
folder = Folder.create(name="My Audio Files")

# Upload a file to the folder
file = File.create(
    localPath="audio.mp3",
    uploadPath="uploaded_audio.mp3", 
    fileName="my_audio_file.mp3",
    folderId=UUID(folder.folderId)
)
# List contents of a folder
folder_contents = Folder.list(path=folder.folderName)

# Copy file to another folder
copy_folder = Folder.create(name="Backup Folder")
copied_file = File.copy(
    fileId=file.fileId,
    currentFolderId=UUID(folder.folderId),
    newFolderId=UUID(copy_folder.folderId)
)

# Update file metadata
updated_file = File.patch(
    fileId=file.fileId,
    file_name="renamed_audio.mp3"
)

# Search for files
search_results = Folder.search(query="audio")

# Get file categories
categories = File.get_file_categories()

# Delete file (simplified - no folderId needed)
File.delete(fileId=file.fileId)
```

#### For Projects and Sessions Integration
```python
# Create a project
project = Project.create(projectName="My Audio Project")

# List all projects
projects = Project.list()

# Create a session within the project
session = Session.create(
    projectId=UUID(project.projectId),
    workflowId="audio_processing_workflow",
    sessionName="Session 1",
    status="active",
    state={"step": "initialization", "progress": 0}
)

# List sessions for a project
sessions = Session.list(projectId=UUID(project.projectId))

# Update session
updated_session = Session.update(
    projectId=UUID(project.projectId),
    sessionId=UUID(session.sessionId),
    sessionName="Updated Session Name",
    status="completed",
    state={"step": "completed", "progress": 100}
)

# Get specific session
retrieved_session = Session.get(
    projectId=UUID(project.projectId),
    sessionId=UUID(session.sessionId)
)

# Delete session
Session.delete(
    projectId=UUID(project.projectId),
    sessionId=UUID(session.sessionId)
)
```

### Breaking Changes Summary

1. **Python version requirement** - Minimum version 3.8 → 3.10
2. **New dependencies** - No new external dependencies added
3. **Files and Folders API v2** - Breaking changes to file and folder operations:
   - `File.create()` now requires `fileName` parameter
   - `File.delete()` simplified to only require `fileId` (no `folderId`)
   - New API endpoints `/files` and `/folders` replace legacy `/v3/file` and `/v3/folder`
   - Response field mappings updated (e.g., `file_id` → `fileId`)
   - Hard link concept introduced for file-folder relationships

## [3.1.0] - 2025-08-04

### Added

- Users are now able to specify the number of retries they would like in an event of a timeout with the aim to provide better automation.
- Users can also specify the timeout threshold with the default value being 300 seconds (5 minutes)
- Added a small delay in between GET requests for speech response to prevent hammering servers.

## [3.0.0] - 2025-07-29

### 🆕 New Features

#### File System Overhaul
- **Complete file system redesign** with hierarchical folder structure
- **New File.Item class** with comprehensive metadata:
  - `fileId`: Unique file identifier
  - `fileName`: Name of the file
  - `url`: Download URL for the file
  - `createdBy`: ID of user who created the file
  - `lastModified`: Last modification timestamp
  - `fileType`: File type information (dict with fileTypeId and name)
  - `fileCategory`: Optional file category (can be null)
  - `size`: File size as string
  - `createdAt`: Creation timestamp
  - `status`: File status (e.g., "uploaded")
  - `duration`: Optional file duration (can be null)

#### New Folder System
- **New Folder.Item class** with hierarchical structure:
  - `folderId`: Unique folder identifier
  - `folderName`: Name of the folder
  - `parentFolderId`: Parent folder ID (empty string for root)
  - `createdBy`: ID of user who created the folder
  - `lastModified`: Optional last modification timestamp (can be null)
  - `createdAt`: Creation timestamp
- **New Folder.ListResponse class** for folder listing operations with:
  - `folders`: List of Folder.Item objects
  - `files`: List of File.Item objects  
  - `currentPathChain`: Dictionary containing path chain information
- **New Folder.get_root_folder_id()` method to get root folder ID

#### Enhanced File Operations
- **Improved file upload process** with automatic polling for completion
- **Timeout handling** using `TIMEOUT_THRESHOLD_S` for upload operations
- **Better error handling** with specific error messages for upload failures

### 🔄 API Changes

#### File.create() Method
- **BREAKING CHANGE**: Parameter names updated:
  - `fileType` → **REMOVED** (no longer needed)
- **New parameter**: `folderId` (Optional[UUID]) for specifying upload location
- **Enhanced behavior**: Now polls for upload completion and returns complete file metadata

#### File.get() Method
- **BREAKING CHANGE**: Parameter name updated:
  - `fileId` → `fileId` (kept camelCase)

#### File.delete() Method
- **BREAKING CHANGE**: Parameter names updated:
  - `fileId` → `fileId` (kept camelCase)
  - `folderId` → `folderId` (kept camelCase, optional, defaults to root folder)
- **Return type change**: Now returns `None` instead of `APIResponseItem`

#### File.Item Attributes
- **BREAKING CHANGE**: All attribute names kept in camelCase:
  - `fileId`: Unique file identifier
  - `fileName`: Name of the file
  - `url`: Download URL for the file
  - `createdBy`: ID of user who created the file
  - `lastModified`: Last modification timestamp
  - `fileType`: File type information (dict with fileTypeId and name)
  - `fileCategory`: Optional file category (can be null)
  - `size`: File size as string
  - `createdAt`: Creation timestamp
  - `status`: File status (e.g., "uploaded")
  - `duration`: Optional file duration (can be null)

#### File.Item.download() Method
- **BREAKING CHANGE**: Now requires `fileName` parameter (no longer optional)

#### Folder Methods
- **Folder.create(name, parentFolderId)** - Create new folder with optional parent
- **Folder.get(folderId)** - Retrieve folder by ID  
- **Folder.delete(folderId)** - Delete folder by ID
- **Folder.get_root_folder_id()** - Get root folder ID

### 🗑️ Removed Features

#### Deprecated Methods
- **File.modify()** - Completely removed
- **File.get_file_categories()** - Completely removed
- **File.get_category_id_by_name()** - Completely removed
- **File.Item.delete()** - Instance method removed (use static method instead)

#### Deprecated Classes
- **Media class** - Completely removed
- **File.List class** - Replaced with Folder.ListResponse
- **Folder.List class** - Replaced with Folder.ListResponse

#### Deprecated Inheritance
- **File.Item** no longer inherits from `APIResponseItem`
- **Folder.Item** no longer inherits from `APIResponseItem`

### 🔧 Technical Improvements

#### Code Quality
- **Comprehensive docstrings** added to all methods and classes (PEP 257 compliant)
- **Type hints** improved throughout the codebase
- **Better error messages** with more descriptive exceptions
- **Fixed typos** in error messages ("eixst" → "exist")

#### Upload Process
- **Fixed upload polling logic** with proper timeout handling
- **Added mime_type parameter** to `send_upload_request` calls
- **Improved upload status checking** with proper boolean logic

### 📝 Migration Guide

#### For File Operations
```python
# OLD
file = File.create(localPath="file.mp3", uploadPath="name.mp3", fileType="audio")
fileId = file.fileId
file.delete(fileId=fileId, folderId=folderId)

# NEW
file = File.create(localPath="file.mp3", uploadPath="name.mp3", folderId=folderId)
fileId = file.fileId
File.delete(fileId=fileId, folderId=folderId)
```

#### For Folder Operations
```python
# OLD
root = Folder.get_root()  # Returns Folder.Item
folderId = root.currentPathChain["folderId"]

# NEW
folderId = Folder.get_root_folder_id()  # Returns string directly
```

#### For File Item Access
```python
# OLD
fileId = file.fileId
fileName = file.fileName

# NEW
fileId = file.fileId  # No change - kept camelCase
fileName = file.fileName  # No change - kept camelCase
```

### ⚠️ Breaking Changes Summary

1. **Parameter names** kept in camelCase (no changes to existing camelCase parameters)
2. **Attribute names** kept in camelCase (no changes to existing camelCase attributes)
3. **File.modify()** method completely removed
4. **File.Item.delete()** instance method removed
5. **Media class** completely removed
6. **File.List and Folder.List** classes removed
7. **Inheritance from APIResponseItem** removed for Item classes
8. **File.create()** now requires `fileName` parameter in download method
9. **Return types** changed for some methods (e.g., delete returns None)
10. **New parameter**: `folderId` added to File.create() for specifying upload location

### 🧪 Testing

- **All existing tests updated** to work with new API
- **New test patterns** for folder operations
- **Conditional test skipping** for staging environment
- **Improved test coverage** for new file system features

## [2.10.1] - 2025-02-24
- Fixed logic that removed 0 float values from payload


## [2.10.0] - 2025-02-13

### Added

- Customer trace id header can now be set per production using the `use_trace` context manager.
- Can pass through custom headers into `send_request`.

## [2.9.0] - 2025-01-23

### Fixed

- Removed emojis from PyPi document
- Made example asset public

## [2.8.2] - 2025-01-22

### Improvement

- Adding custom loudness presets support.

## [2.8.0] - 2025-01-20

### Added

- Added Voice query endpoint to SDK.

## [2.7.1] - 2024-12-18

### Improvement

- Adding a default timeout of 300 seconds for polls. 

## [2.7.0] - 2024-11-20

### Added

- Sound template endpoint for recommendation.

## [2.6.0] - 2024-10-31

### Added

- IAB endpoint added to SDK.

## [2.5.1] - 2024-10-31

### Fixed

- Hardened video endpoint tests
- Excluded the tests directory (which has some audio and video fixtures) from final build to keep package size down.


## [2.5.0] - 2024-09-27

### Added

- Transcribe endpoint added to SDK.

## [2.4.0] - 2024-09-13

### Added

- useAutoFix parameter for tts requests

## [2.3.0] - 2024-07-31

### Added

- useDenoiser parameter for tts requests
  
## [2.2.0] - 2024-07-24

### Added

- useCache parameter for tts requests

## [2.1.0] - 2024-07-08

### Added

- Speech-To-Speech integration.


## [2.0.6] - 2024-07-08

### Fixes

Add generic sections to request body


## [2.0.5] - 2024-07-08

### Fixes

Fix sections


## [2.0.4] - 2024-07-08

### Fixes

Add sections to production mix for atmosphere per section input through param.


## [2.0.3] - 2024-06-24

### Fixes

Improved error messaging for Media files


## [2.0.0] - 2024-05-20

### Breaking change 

- Updated project to be compatible only with python `^3.8.1`

### Fixes

- Fixed missing argument in `content.list_modules`.
- Fixed inclusion of missing `x-assume-org` header in `request_interface.download_url`.