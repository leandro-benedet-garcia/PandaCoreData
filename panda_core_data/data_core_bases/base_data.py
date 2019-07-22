'''
:created: 2019-07-22

:author: Leandro (Cerberus1746) Benedet Garcia
'''

import sys, inspect

from dataclasses import dataclass
from glob import iglob
from os.path import join
from pathlib import Path
from importlib import import_module


from ..custom_exceptions import (PCDTypeGroupNotFound, PCDTypeNotFound, PCDDuplicatedTypeName,
                                 PCDInvalidBaseData)

@dataclass(repr=False)
class Group(dict):
    """Class that is used to store Models or Templates"""
    group_name: str

    def __repr__(self):
        #pylint: disable=no-member
        fields = [f"{field_name}({field_type}) = {getattr(self, field_name)}"
                  for field_name, field_type in self.__annotations__.items()]

        to_return = []
        to_return += "Group:"
        to_return += ', '.join(fields)
        to_return += super().__repr__()

        return "\n".join(to_return)


class BaseData(object):
    def __init_subclass__(cls):  # @NoSelf
        if cls.__name__ == "DataCore":
            return

        data_type = cls.__name__.lower().replace("data", "")

        cls_attributes = dir(cls)
        base_attributes = dir(BaseData)

        for original_attr in base_attributes:
            if "data" not in original_attr:
                continue

            current_attribute = original_attr.replace("data", data_type)

            if current_attribute not in cls_attributes:
                raise PCDInvalidBaseData(f"The class '{cls.__name__}' doesn't have the attribute "
                                         f"{current_attribute}")

            base_docstring = getattr(BaseData, original_attr).__doc__
            if base_docstring:
                base_docstring = base_docstring.replace("Data", data_type.capitalize())
                base_docstring = base_docstring.replace("data", data_type)

                getattr(cls, current_attribute).__doc__ = base_docstring

    @staticmethod
    def get_data_group(name: str, group_dict, default):
        group = group_dict.get(name, default)
        if not group and default is None:
            raise PCDTypeGroupNotFound(f"Group '{name}' could not be found.")

        return group

    @staticmethod
    def get_or_create_data_group(name: str, group_dict):
        """
        Get or create the data group. If it doesn't exist, it will be created.

        :param name: Name of the group.
        :type name: str
        """
        return group_dict.setdefault(name, Group(name))

    def get_data_type(self, name: str, group_dict, group_name: str, default,
                                group_default):
        """
        Get Data type from the specified group.

        :param name: Name of the Data type.
        :type name: str
        :param group_name: Name of the group.
        :type group_name: str
        :param default: Default value to return if the Data type couldn't be found.
        :type default: any
        :param group_default: Default value to return if the group couldn't be found.
        :type group_default: any
        """
        group = self.get_data_group(group_name, group_dict, default=group_default)
        if group:
            model = group.get(name, default)
            if not model and default is None:
                raise PCDTypeNotFound(f"Model type {name} could not be found inside "
                                      f"the group {group_name}")
            return model
        return default

    @staticmethod
    def add_data_module(path, module_type):
        """
        Recursively add a data module from the supplied path.

        :param path: Path to the data module
        :type path: str
        """
        sys.path.append(path)

        for py_file in iglob(join(path, '*.py')):
            module_name = Path(py_file).stem
            module_type.append(import_module(module_name))

    def add_data_to_group(self, group_name: str, data, group_dict, auto_create_group, replace):
        """
        Add the supplied Data type to the group.

        :param group_name: Name of the group
        :type group_name: str
        :param data: The Data type to be added.
        :type data: Data
        :param auto_create_group: If the group should be automatically created if it doesn't exist.
        :type auto_create_group: bool
        :param replace: If the Data type should be replaced if it already exists.
        :type replace: bool
        """
        name = data.data_name
        if auto_create_group:
            group = self.get_or_create_data_group(group_name, group_dict)
        else:
            group = self.get_data_group(group_name, group_dict, None)

        if not replace and name in group:
            raise PCDDuplicatedTypeName(f"There's already a {type(data)} with the name {name} "
                                        f"inside the group {group_name}.")

        data.data_group = group
        group[name] = data
        return group
