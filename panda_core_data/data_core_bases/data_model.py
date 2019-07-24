'''
:created: 2019-07-22

:author: Leandro (Cerberus1746) Benedet Garcia
'''
from .base_data import BaseData, Group

class DataModel(BaseData):
    model_modules = []
    raw_models = []
    raw_model_folders = []

    all_model_groups = Group("all_model_groups")
    all_key_value_models = Group("all_key_value_models")

    @property
    def all_models(self):
        """Get all model types"""
        return list(self.all_key_value_models.values())

    def get_model_from_all(self, model_name):
        return self.get_data_from_all(model_name, self.all_key_value_models)

    def recursively_instance_model(self, path):
        self.recursively_instance_data(path, self.get_model_from_all)

    def get_or_create_model_group(self, name: str):
        return self.get_or_create_data_group(name, self.all_model_groups)

    def get_model_group(self, **kwargs):
        return self.get_data_group(self.all_model_groups, **kwargs)

    def add_model_module(self, path):
        self.add_data_module(path, self.model_modules)

    def add_model_to_group(self, group_name: str, model, **kwargs):
        self.add_data_to_group(group_name, model, self.get_model_group,
                               self.get_or_create_model_group, **kwargs)

    def get_model_type(self, name: str, **kwargs):
        return self.get_data_type(name, self.get_model_group, **kwargs)
