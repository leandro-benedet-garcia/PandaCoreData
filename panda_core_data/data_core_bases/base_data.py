'''
:created: 2019-07-22

:author: Leandro (Cerberus1746) Benedet Garcia
'''

import sys

from dataclasses import dataclass
from glob import iglob
from os.path import join
from pathlib import Path
from importlib import import_module

from . import DEFAULT_DATA_GROUP
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
        to_return.append("Group:")
        to_return.append(', '.join(fields))
        to_return.append(super().__repr__())

        return "\n".join(to_return)

@dataclass(repr=False)
class GroupInstance(Group):
    data_type: "ModelMixin"

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
    def get_data_group(group_dict, name: str = DEFAULT_DATA_GROUP, group_default=None):
        group = group_dict.get(name, group_default)
        if not group and group_default is None:
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

    @staticmethod
    def recursively_instance_data(path, from_all_method):
        for raw_file in iglob(join(path, '*.yaml')):
            raw_data_name = Path(raw_file).stem
            template_type = from_all_method(raw_data_name)
            template_type.instance_from_raw(raw_file)

    @staticmethod
    def get_data_type(name: str, group_method, **kwargs):
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
        default = kwargs.pop("default", None)
        group = group_method(group_default=kwargs.pop("group_default", None), **kwargs)
        if group:
            data_type = group.get(name, default)
            if not data_type and default is None:
                raise PCDTypeNotFound(f"Model type {name} could not be found inside "
                                      f"the group {kwargs.get('group_name', DEFAULT_DATA_GROUP)}")
            return data_type
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

    @staticmethod
    def get_data_from_all(data_name, data_dict):
        return data_dict[data_name]

    @staticmethod
    def add_data_to_group(group_name: str, data, data_group_method, get_or_create_data_group,
                          auto_create_group=True, replace=False):
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
            group = get_or_create_data_group(group_name)
        else:
            group = data_group_method(name=group_name, group_default=None)

        if not replace and name in group:
            raise PCDDuplicatedTypeName(f"There's already a {type(data)} with the name {name} "
                                        f"inside the group {group_name}.")

        data.data_group = group
        group[name] = data
        return group