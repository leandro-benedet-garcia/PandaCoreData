'''
:created: 2019-07-22

:author: Leandro (Cerberus1746) Benedet Garcia
'''

from glob import iglob
from os.path import join
from pathlib import Path

from .base_data import BaseData, Group

class DataModel(BaseData):
    def __init__(self):
        self.model_modules = []
        self.raw_models = []
        self.raw_model_folders = []

        self.all_model_groups = Group("all_model_groups")
        self.all_model_types = Group("all_model_types")
        self.all_model_intances = Group("all_model_intances")

    @property
    def all_models(self):
        """Get all model types"""
        return list(self.all_model_types.values())

    def get_all_model_instances(self):
        for instance_group in self.all_model_intances.values():
            for current_instance in instance_group:
                yield current_instance

    def instance_model(self, data_type_name, path, **kwargs) -> "Model":
        self.raw_models.append(Path(path))
        return self.instance_data(data_type_name, path, self.get_model_type, **kwargs)

    def get_model_from_all(self, model_name, **kwargs):
        return self.get_data_from_all(model_name, self.all_model_types, **kwargs)

    def recursively_instance_model(self, path, *args, **kwargs):
        """
        Instance Model recursively based on the raws inside the folders.

        :param path: Starting path to search for raws.
        :type path: str
        """
        instanced_data = []
        root_model = Path(path)
        for model_path in root_model.iterdir():
            if model_path.is_dir():
                for raw_file in iglob(join(model_path, '*.yaml')):
                    instanced_data.append(self.instance_model(model_path.stem, raw_file, *args,
                                                              **kwargs))

        return instanced_data

    def get_or_create_model_group(self, name: str):
        return self.get_or_create_data_group(name, self.all_model_groups)

    def get_model_group(self, **kwargs):
        return self.get_data_group(self.all_model_groups, **kwargs)

    def add_model_module(self, path):
        self.add_data_module(path, self.model_modules)

    def add_model_to_group(self, group_name: str, model, **kwargs):
        self.add_data_to_group(group_name, model, self.get_model_group,
                               self.get_or_create_model_group,
                               self.all_model_intances, **kwargs)

    def get_model_type(self, name: str, **kwargs):
        return self.get_data_type(name, self.get_model_group, **kwargs)
