# Change Log
All notable changes to `audiostack` will be documented in this file.
 
The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [2.10.0] - 2025-02-13

### Added

- Customer trace id header can now be set.

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