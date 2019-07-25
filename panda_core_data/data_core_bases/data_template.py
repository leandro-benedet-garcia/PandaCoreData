'''
:created: 2019-07-22

:author: Leandro (Cerberus1746) Benedet Garcia
'''

from .base_data import BaseData, Group, GroupInstance

class DataTemplate(BaseData):
    '''classdocs'''
    template_modules = []
    raw_templates = []
    raw_template_folders = []

    all_template_groups = Group("all_template_groups")
    all_key_value_templates = Group("all_key_value_templates")
    all_template_instances = GroupInstance("all_template_instances", None)

    @property
    def all_templates(self):
        """Get all model types"""
        return list(self.all_key_value_templates.values())

    def get_template_instances(self):
        return self.all_template_instances.values()

    def get_template_from_all(self, model_name, **kwargs):
        return self.get_data_from_all(model_name, self.all_key_value_templates, **kwargs)

    def instance_template(self, data_type_name, path, **kwargs) -> "Template":
        return self.instance_data(data_type_name, path, self.get_template_type, generate_id=False,
                                  **kwargs)

    def recursively_instance_template(self, path):
        self.recursively_instance_data(path, self.instance_template)

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
