'''
:created: 2019-07-22

:author: Leandro (Cerberus1746) Benedet Garcia
'''
from pathlib import Path

from ..storages import raw_glob_iterator
from .base_data import BaseData, Group


class DataTemplate(BaseData):
    def __init__(self, *args, **kwargs):
        self.raw_templates = []
        self.raw_template_folders = []

        self.all_template_groups = Group("all_template_groups")
        self.all_key_value_templates = Group("all_key_value_templates")
        super().__init__(*args, **kwargs)

    @property
    def all_templates(self):
        return list(self.all_key_value_templates.values())

    @property
    def all_template_instances(self):
        """
        Gets all the template instances

        :yield Template: returns a generator of all instanced templates.
        """
        for template_type in self.all_templates:
            yield template_type.instanced()

    def get_template_type(self, template_name, **kwargs):
        return self.get_data_type(template_name, self.all_key_value_templates, **kwargs)

    def instance_template(self, data_type_name, path, **kwargs) -> "Template":
        return self.instance_data(data_type_name, self.get_template_type, path, **kwargs)

    def recursively_instance_template(self, path, *args, **kwargs):
        instanced_data = []
        for raw_file in raw_glob_iterator(path, self.excluded_extensions):
            raw_data_name = Path(raw_file).stem
            instanced = self.instance_template(raw_data_name, raw_file, *args, **kwargs)
            instanced_data.append(instanced)

        return instanced_data
