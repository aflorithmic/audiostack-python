# Change Log
All notable changes to `audiostack` will be documented in this file.
 
The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

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
