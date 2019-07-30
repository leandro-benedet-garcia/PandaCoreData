'''
:created: 2019-07-22

:author: Leandro (Cerberus1746) Benedet Garcia
'''

import sys
from dataclasses import dataclass
from glob import iglob
from os.path import join
from importlib import import_module


from ..custom_exceptions import PCDTypeNotFound, PCDInvalidBaseData
from ..utils import auto_convert_to_pathlib

@dataclass(repr=False)
class Group(dict):
    """Class that is used to store :class:`Model` or :class:`Template` classes"""
    group_name: str

@dataclass(repr=False)
class GroupInstance(list):
    """Class that is used to store Instances"""
    data_type: "DataType"

@dataclass(repr=False)
class GroupWrapper(object):
    """Class that is used to store Models or Templates"""
    data_type: "DataType"
    instances: GroupInstance = None

    def __post_init__(self):
        self.instances = GroupInstance(self.data_type)

    def __repr__(self):
        return f"Wrapper of {type(self.data_type.data_name).__name__}: \n\t{repr(self.instances)}"

class BaseData(object):
    def __init_subclass__(cls):  # @NoSelf
        """
        This function checks if a method is lacking inside any class that inherits this, and also
        automatically creates docstrings into those methods based on the original method.

        :param DataType cls: Child class
        """

        # The only class that don't go trough the check is DataCore
        if cls.__name__ == "DataCore":
            return

        data_type = cls.__name__.lower().replace("data", "")

        cls_attributes = dir(cls)
        base_attributes = dir(BaseData)
        changed_attrs = []

        for original_attr in base_attributes:
            if "data" not in original_attr:
                continue
            changed_attrs.append([original_attr, 0])
            current_attribute = original_attr.replace("data", data_type)

            if current_attribute not in cls_attributes:
                raise PCDInvalidBaseData(f"The class '{cls.__name__}' doesn't have the attribute "
                                         f"{current_attribute}")

            base_docstring = getattr(BaseData, original_attr).__doc__
            if base_docstring:
                base_docstring = base_docstring.replace("DataType", data_type.capitalize())
                base_docstring = base_docstring.replace("data", data_type)

                getattr(cls, current_attribute).__doc__ = base_docstring

    @staticmethod
    def all_datas():
        """
        Get all :class:`DataType` types

        :return list(DataType): return a list of data types.
        """

    @staticmethod
    def recursively_add_data_module(path, module_type):
        """
        Recursively add a module with :class:`DataType` from the supplied path.

        :param str path: Path to the data module
        :return list(module): Returns the loaded modules.
        """
        added_modules = []
        path = auto_convert_to_pathlib(path, True)

        for py_file in iglob(join(path, '*.py')):
            module_full_path = auto_convert_to_pathlib(py_file, False)
            module_name = module_full_path.stem
            module_path = str(module_full_path.parent)
            if module_path not in sys.path:
                sys.path.append(module_path)

            try:
                imported_module = import_module(module_name)
            except ModuleNotFoundError as module_error:
                raise ModuleNotFoundError(f"{module_error} with the base_path '{path}' sys.path "
                                          f"'{sys.path}'")
            module_type.append(imported_module)

        module_type += added_modules
        return added_modules

    @staticmethod
    def get_data_type(data_name, data_dict, default=None):
        """
        Get Data type from a list of all :class:`DataType` types.

        :param str data_name: The name of the DataType
        :param bool default: Default value to be returned if the data type couldn't be found.
        :return DataType: the :class:`DataType`
        """
        data_type = data_dict.get(data_name, default)
        if not data_type and default is None:
            raise PCDTypeNotFound(f"Data type {data_name} could not be found. The available "
                                  f"templates are {list(data_dict.values())}")

        return data_type

    @staticmethod
    def recursively_instance_data():
        """
        Instance :class:`DataType` recursively based on the raws inside the folders.

        :param str path: Starting path to search for raws.
        :return list(DataType): returns all the instanced data from the path.
        """
