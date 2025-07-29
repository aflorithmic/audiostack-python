# Change Log
All notable changes to `audiostack` will be documented in this file.
 
The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

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