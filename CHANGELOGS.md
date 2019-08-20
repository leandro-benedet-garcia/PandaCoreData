# Change Logs

## 0.0.4
### Added
- Support for tox

### Changed
- Fixed the installer to behave better, which could derp while reading some files.

## 0.0.3
### Changed
- Improved compatibility with Python.Net

### Fixed
- Fixed a bug with the `_get_core()` method

## 0.0.2
### Added
- Support for Json was added
- Now, it's possible to save the [Model](https://pandacoredata.readthedocs.io/en/latest/api/data_type.html#panda_core_data.model.Model) or [Template](https://pandacoredata.readthedocs.io/en/latest/api/data_type.html#panda_core_data.model.Template) to the raw with the `save_to_file` method
- `instance_data` and `older_contents` were added.
- `panda_core_data_commands` has a new option `-re` which you can choose between `json` or `yaml`
- [PCDInvalidRaw](https://pandacoredata.readthedocs.io/en/latest/api/custom_exceptions.html#panda_core_data.custom_exceptions.PCDInvalidRaw) and [PCDDuplicatedModuleName](https://pandacoredata.readthedocs.io/en/latest/api/custom_exceptions.html#panda_core_data.custom_exceptions.PCDDuplicatedModuleName) exceptions was created
- Package `Storage` was created

### Changed
- [auto_convert_to_pathlib](https://pandacoredata.readthedocs.io/en/latest/api/storage.html#panda_core_data.storages.auto_convert_to_pathlib) do not need the `is_file` parameter anymore
- [DataCore](https://pandacoredata.readthedocs.io/en/latest/api/core_data.html#panda_core_data.DataCore) has a new parameter `excluded_extensions`
- Both exceptions `PCDFolderNotFound` and `PCDFileNotFound` was merged into [PCDInvalidPath](https://pandacoredata.readthedocs.io/en/latest/api/custom_exceptions.html#panda_core_data.custom_exceptions.PCDInvalidPath)

## 0.0.1
### Added
- Package released
- Basic yaml reading which their contents is loaded to a python `dataclass`
