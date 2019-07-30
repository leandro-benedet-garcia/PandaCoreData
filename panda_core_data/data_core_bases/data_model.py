'''
:created: 2019-07-22

:author: Leandro (Cerberus1746) Benedet Garcia
'''

from .base_data import BaseData, Group
from ..custom_exceptions import PCDFolderIsEmpty, PCDInvalidPathType
from ..utils import auto_convert_to_pathlib

class DataModel(BaseData):
    def __init__(self):
        self.raw_models = []
        self.raw_model_folders = []

        self.all_model_groups = Group("all_model_groups")
        self.all_model_types = Group("all_model_types")
        self.all_model_intances = Group("all_model_intances")

    @property
    def all_models(self):
        return list(self.all_model_types.values())

    @property
    def all_model_instances(self):
        """
        Gets all the model instances.

        :yield Model: returns a generator of all instanced templates.
        """
        for current_type in self.all_models:
            for current_instance in current_type.all_instances:
                yield current_instance

    def instance_model(self, model_type_name, path, **kwargs):
        path = auto_convert_to_pathlib(path, False)
        self.raw_models.append(path)

        data_type = self.get_model_type(model_type_name, **kwargs)
        instanced = data_type.instance_from_raw(path)

        data_type.wrapper.instances.append(instanced)
        return instanced

    def get_model_type(self, model_name: str, **kwargs):
        return self.get_data_type(model_name, self.all_model_types, **kwargs)

    def recursively_instance_model(self, path, *args, **kwargs):
        instanced_data = []
        root_model = auto_convert_to_pathlib(path, True)
        folder_contents = list(root_model.iterdir())

        if not any(folder_contents):
            raise PCDFolderIsEmpty(f"The folder {path} is empty")

        for model_path in folder_contents:
            if model_path.is_file():
                raise PCDInvalidPathType(f"The path '{model_path}' must be a folder and needs to "
                                         "have a model name.")
            for raw_file in model_path.glob('*.yaml'):
                instanced = self.instance_model(model_path.stem, raw_file, *args, **kwargs)
                instanced_data.append(instanced)

        return instanced_data
