'''
:created: 2019-07-22

:author: Leandro (Cerberus1746) Benedet Garcia
'''

from .base_data import BaseData, Group
from . import DEFAULT_DATA_GROUP

class DataTemplate(BaseData):
    '''classdocs'''
    template_modules = []
    raw_templates = []
    raw_template_folders = []

    all_template_groups = Group("all_template_groups")
    all_key_value_templates = Group("all_key_value_templates")

    @property
    def all_templates(self):
        """Get all template types"""
        return list(self.all_key_value_templates.values())

    def get_template_from_all(self, template_name):
        return self.get_data_from_all(template_name, self.all_key_value_templates)

    def recursively_instance_template(self, path):
        self.recursively_instance_data(path, self.get_template_from_all)

    def get_or_create_template_group(self, name: str):
        return self.get_or_create_data_group(name, self.all_template_groups)

    def get_template_group(self, name: str, default=None):
        return self.get_data_group(name, self.all_template_groups, default)

    def add_template_module(self, path):
        self.add_data_module(path, self.template_modules)

    def get_template_type(self, name: str, group_name: str = DEFAULT_DATA_GROUP, default=None,
                          group_default=None):
        return self.get_data_type(name, self.all_template_groups, group_name, default,
                                  group_default)

    def add_template_to_group(self, group_name: str, template, **kwargs):
        self.add_data_to_group(group_name, template, self.get_template_group,
                               self.get_or_create_template_group, **kwargs)
