Any notable and major updates will be listed here going forward.

# Changelog

## Update on Jan 31st

### Changed

* Log.txt and log file in the UI box now read from newest to oldest.

### Added

* Added support for multiple generated prompts in one click for A1111 and Invoke outputs.

### Removed

N/A

### Fixes

* Major performance fix for logging. When generating multiple-numerous prompts at once, the log would often only get a partial output. This is now fixed for logs.txt as well as the A1111 and Invoke logs. You should be able to generate dozens of prompts in one go without issue.
