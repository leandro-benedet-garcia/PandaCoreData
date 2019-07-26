'''
:created: 2019-07-22

:author: Leandro (Cerberus1746) Benedet Garcia
'''
from glob import iglob
from os.path import join
from pathlib import Path

from .base_data import BaseData, Group, GroupInstance

class DataTemplate(BaseData):
    '''classdocs'''
    def __init__(self):
        self.template_modules = []
        self.raw_templates = []
        self.raw_template_folders = []
    
        self.all_template_groups = Group("all_template_groups")
        self.all_key_value_templates = Group("all_key_value_templates")
        self.all_template_instances = GroupInstance("all_template_instances", None)

    @property
    def all_templates(self):
        """Get all model types"""
        return list(self.all_key_value_templates.values())

    def get_all_template_instances(self):
        return list(self.all_template_instances.values())

    def get_template_from_all(self, model_name, **kwargs):
        return self.get_data_from_all(model_name, self.all_key_value_templates, **kwargs)

    def instance_template(self, data_type_name, path, **kwargs) -> "Template":
        self.raw_templates.append(Path(path))
        return self.instance_data(data_type_name, path, self.get_template_type, generate_id=False,
                                  **kwargs)

    def recursively_instance_template(self, path, *args, **kwargs):
        """
        Instance Template recursively based on the raws inside the folders.

        :param path: Starting path to search for raws.
        :type path: str
        """
        instanced_data = []
        for raw_file in iglob(join(path, '*.yaml')):
            raw_data_name = Path(raw_file).stem
            instanced_data.append(self.instance_template(raw_data_name, raw_file, *args, **kwargs))

        return instanced_data

    def get_or_create_template_group(self, name: str):
        return self.get_or_create_data_group(name, self.all_template_groups)

    def get_template_group(self, **kwargs):
        return self.get_data_group(self.all_template_groups, **kwargs)

    def add_template_module(self, path):
        self.add_data_module(path, self.template_modules)

    def get_template_type(self, name: str, **kwargs):
        return self.get_data_type(name, self.get_template_group, **kwargs)

    def add_template_to_group(self, group_name: str, template, **kwargs):
        self.add_data_to_group(group_name, template, self.get_template_group,
                               self.get_or_create_template_group,
                               self.all_template_instances, **kwargs)
