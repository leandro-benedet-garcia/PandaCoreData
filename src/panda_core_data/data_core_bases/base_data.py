'''
:created: 2019-07-22

:author: Leandro (Cerberus1746) Benedet Garcia
'''
from dataclasses import dataclass
from glob import iglob
from importlib import import_module
from os.path import join
import sys
from types import ModuleType
from typing import Optional, Dict, List, Callable, Union

from ..custom_exceptions import (PCDTypeError, PCDInvalidBaseData,
                                 PCDFolderIsEmpty, PCDDuplicatedModuleName)
from ..custom_typings import PathType
from ..data_type import DataType
from ..storages import auto_convert_to_pathlib


@dataclass(repr=False)
class Group(dict):
    """
    Class that is used to store :class:`~panda_core_data.model.Model` or
    :class:`~panda_core_data.model.Template` classes
    """
    group_name: str


@dataclass(repr=False)
class GroupInstance(list):
    """Class that is used to store Instances"""
    data_type: DataType


@dataclass(repr=False)
class GroupWrapper():
    """Class that is used to store Models or Templates"""
    data_type: DataType
    instances: Optional[GroupInstance] = None

    def __post_init__(self):
        self.instances = GroupInstance(self.data_type)

    def __repr__(self) -> str:
        type_name = self.data_type.data_name
        the_type = self.data_type.__name__
        if type_name != the_type:
            return f"Wrapper of {type_name} ({the_type}): " \
                   f"\n\t{repr(self.instances)}"
        return f"Wrapper of {type_name}: \n\t{repr(self.instances)}"


IMPORTED_DATA_MODULES: Dict[str, ModuleType] = {}


class BaseData():
    def __init__(self, excluded_extensions: Union[bool, str] = False):
        self._raw_extensions = []
        self.excluded_extensions = excluded_extensions

    def __init_subclass__(cls):
        """
        This function checks if a method is lacking inside any class that
        inherits this, and also automatically creates docstrings into those
        methods based on the original method.
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
                raise PCDInvalidBaseData(
                    f"The class '{cls.__name__}' doesn't have the attribute "
                    f"{current_attribute}")

            base_docstring = getattr(BaseData, original_attr).__doc__
            if base_docstring:
                base_docstring = base_docstring.replace(
                    "DataType", data_type.capitalize())
                base_docstring = base_docstring.replace("data", data_type)

                getattr(cls, current_attribute).__doc__ = base_docstring

    @staticmethod
    def all_datas() -> List[DataType]:
        """
        Get all :class:`~panda_core_data.model.DataType` types

        :return: return a list of data types.
        """

    @staticmethod
    def folder_contents(path: 'panda_core_data.PathType'):
        root_data = auto_convert_to_pathlib(path)
        contents = list(root_data.iterdir())

        if not any(contents):
            raise PCDFolderIsEmpty(f"The folder {path} is empty")

        return contents

    @staticmethod
    def add_module(path: PathType) -> ModuleType:
        """
        Automatically import the module from the python file and add it's
        directory to `sys.path` if it wasn't in there before.

        :param path: The path to the python file.
        :return module: Returns the imported module.
        """
        module_full_path = auto_convert_to_pathlib(path)
        module_name = module_full_path.stem
        module_path = str(module_full_path.parent)

        if module_name in IMPORTED_DATA_MODULES:
            raise PCDDuplicatedModuleName("A data module with the name "
                                          f"{module_name} was already imported")

        if module_path not in sys.path:
            sys.path.append(module_path)
        try:
            imported_module = import_module(module_name)
            IMPORTED_DATA_MODULES[module_name] = imported_module
            return imported_module
        except ModuleNotFoundError as module_error:  # pragma: no cover
            raise ModuleNotFoundError(f"{module_error} with the base_path"
                                      f"'{path}' sys.path '{sys.path}'")

    def recursively_add_module(self, path: PathType) -> List[ModuleType]:
        """
        Recursively add a module with :class:`~panda_core_data.model.DataType`
        from the supplied path.

        :param str path: Path to the data module
        """
        added_modules = []
        path = auto_convert_to_pathlib(path)

        for py_file in iglob(join(path, '*.py')):
            current_module = self.add_module(py_file)
            added_modules.append(current_module)

        return added_modules

    @staticmethod
    def get_data_type(data_name: str, data_dict, default: Optional[bool] = None
                      ) -> DataType:
        """
        Get Data type from a list of all
        :class:`~panda_core_data.model.DataType` types.

        :param data_name: The name of the DataType
        :param default: Default value to be returned if the data type
                             couldn't be found.
        :return: the :class:`~panda_core_data.model.DataType`
        """
        data_type = data_dict.get(data_name, default)
        if not data_type and default is None:
            raise PCDTypeError(
                f"Data type {data_name} could not be found. The available "
                f"templates are {list(data_dict.values())}")

        return data_type

    @staticmethod
    def instance_data(data_name: str, get_data_type: Callable, path: PathType,
                      **kwargs) -> DataType:
        """
        Create a new instance of a :class:`~panda_core_data.model.DataType`

        :param data_type_name: name of the DataType
        :param path: path to the raw file
        :return: The instanced :class:`~panda_core_data.model.DataType`
        """
        path = auto_convert_to_pathlib(path)
        data_type = get_data_type(data_name, **kwargs)

        instanced = data_type.instance_from_raw(path)
        instanced.raws.append(path)

        return instanced

    @staticmethod
    def recursively_instance_data() -> List[DataType]:
        """
        Instance :class:`~panda_core_data.model.DataType` recursively based on
        the raws inside the folders.
        """
