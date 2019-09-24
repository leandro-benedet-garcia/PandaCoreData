'''
:created: 2019-07-22
:author: Leandro (Cerberus1746) Benedet Garcia
'''
from typing import Iterator, Tuple

#pylint: disable=unused-import
import panda_core_data
#pylint: disable=unused-import
import panda_core_data.model

from ..custom_exceptions import PCDInvalidPathType
from ..storages import is_excluded_extension, raw_glob_iterator
from .base_data import BaseData, Group


class DataModel(BaseData):
    def __init__(self, *args, **kwargs):
        self.raw_models = []
        self.raw_model_folders = []

        self.all_model_groups = Group("all_model_groups")
        self.all_model_types = Group("all_model_types")
        self.all_model_intances = Group("all_model_intances")
        super().__init__(*args, **kwargs)

    @property
    def all_models(self) -> Tuple['panda_core_data.model.Model']:
        return tuple(self.all_model_types.values())

    @property
    def all_model_instances(self) -> Iterator['panda_core_data.model.Model']:
        """
        Gets all the model instances.

        :yield Model: returns a generator of all instanced templates.
        """
        for current_type in self.all_models:
            for current_instance in current_type.all_instances:
                yield current_instance

    def instance_model(self, data_type_name: str,
                       path: 'panda_core_data.PathType', **kwargs
                       ) -> 'panda_core_data.model.Model':
        return self.instance_data(data_type_name, self.get_model_type,
                                  path, **kwargs)

    def get_model_type(self, model_name: str, **kwargs
                       ) -> 'panda_core_data.model.Model':
        return self.get_data_type(model_name, self.all_model_types, **kwargs)

    def recursively_instance_model(self, path: 'panda_core_data.PathType',
                                   *args, **kwargs
                                   ) -> Iterator['panda_core_data.model.Model']:
        instaced_models = []
        for model_path in self.folder_contents(path):
            is_excluded = is_excluded_extension(model_path,
                                                self.excluded_extensions)
            if model_path.is_file() and not is_excluded:
                raise PCDInvalidPathType(f"The path '{model_path}' must be a "
                                         "folder and needs to  have a model "
                                         "name.")

            for raw_file in raw_glob_iterator(model_path,
                                              self.excluded_extensions):
                instaced_models.append(self.instance_model(model_path.stem,
                                                           raw_file, *args,
                                                           **kwargs))
            return instaced_models
