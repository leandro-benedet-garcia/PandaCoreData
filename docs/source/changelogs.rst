Change Logs
============

0.0.2
------
* Support for Json was added
* :func:`~panda_core_data.storages.auto_convert_to_pathlib` do not need the `is_file` parameter
  anymore
* :class:`~panda_core_data.DataCore` has a new parameter `excluded_extensions`
* Now, it's possible to save the :class:`~panda_core_data.model.Model` or
  :class:`~panda_core_data.model.Template` to the raw with the
  :meth:`~panda_core_data.data_type.DataType.save_to_file` method
* :class:`~panda_core_data.custom_exceptions.PCDInvalidRaw` and
  :class:`~panda_core_data.custom_exceptions.PCDDuplicatedModuleName` exceptions was created
* :meth:`~panda_core_data.base_data.BaseData.instance_data` and
  :meth:`~panda_core_data.base_data.BaseData.folder_contents` were added.
* `panda_core_data_commands` has a new option `-re` which you can choose between `json` or `yaml`
* Both exceptions `PCDFolderNotFound` and `PCDFileNotFound` was merged into :class:`PCDInvalidPath`
* Package `Storage` was created