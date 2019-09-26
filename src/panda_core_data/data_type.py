'''This is the heart of Models and Templates

:created: 2019-04-30
:author: Leandro (Cerberus1746) Benedet Garcia'''
from dataclasses import dataclass, _process_class, fields
from inspect import signature
from typing import Any, Optional, Dict, Union, List

from tinydb import TinyDB
from tinydb.queries import Query

# pylint: disable=unused-import
import panda_core_data

from .custom_exceptions import (PCDDuplicatedTypeName, PCDTypeError,
                                PCDNeedsToBeInherited, PCDKeyError)
from .custom_typings import PathType
from .storages import (auto_convert_to_pathlib, get_storage_from_extension,
                       get_extension)
from .utils import check_if_valid_instance


class DataType(TinyDB):
    """Base for all the model types, be it template or model

    Internally it uses the TinyDB database"""
    __weakref__ = ("_current_index", "_keys_cache")

    DEFAULT_TABLE: str = 'data'
    parents: Dict[str, "DataType"] = {}
    query: Query = Query()
    raws: list = []

    data_name: str = "DataType"

    dependencies: List[str]
    data_group: "Group"
    data_core: "DataCore"
    wrapper: "GroupWrapper"

    _current_index: int = -1
    _keys_cache: List[str] = []

    def __new__(cls, *_, db_file: Optional[PathType] = None, **__):
        """Method that handles the instancing of the models and templates, this
        is necessary because dataclasses create a custom __init__ method. Which
        we doesn't use at all if a raw file is supplied."""
        if not hasattr(cls, "dataclass_args"):
            raise PCDNeedsToBeInherited("You can't create a DataType instance "
                                        "directly without inheriting it first.")

        instanced = object.__new__(cls)
        instanced.dataclass_instanced = not isinstance(db_file, str)

        return instanced

    def __getattr__(self, attr_name: str) -> Any:
        """This is here just to make this method back to the default that was
        overwritten by TinyDB

        :param name: name of the attribute to get"""
        raise AttributeError(f"type object '{type(self).__name__}' has no "
                             f"attribute '{attr_name}'")

    __setattr__ = object.__setattr__

    def __repr__(self) -> str:
        return_value = []
        fields_list = fields(self)
        fields_list = ["\t\t{}({}) = {}".format(
            current_field.name,
            current_field.type,
            getattr(self, current_field.name)) for current_field in fields_list]

        if self.data_name != type(self).__name__:
            return_value.append(
                f"DataType {self.data_name} ({type(self).__name__}):")
        else:
            return_value.append(f"DataType {self.data_name}:")

        return_value.append("\tFields:")
        return_value.append('\n'.join(fields_list))

        # if any(self.parents):
        #    checked_parents = [self.data_name,]
        #    return_value.append("\tParents:")
        #    for parent_name, parent_value in self.parents.items():
        #        if parent_name in checked_parents:
        #            continue
        #        checked_parents.append(parent_name)
        #        return_value.append("\t\t" + parent_name + "\n\t\t\t" +
        # repr(parent_value).replace("\n", "\n\t\t\t"))

        return "\n".join(return_value)

    def __bool__(self) -> bool:
        return self.is_instanced

    # mapping helpers ----------------------------------------------------------
    def _in_fields(self, key: str):
        if key in self:
            return getattr(self, key)
        raise PCDKeyError(key)

    def _set_field(self, key: str, value: Any):
        if key in self:
            return setattr(self, key, value)
        raise PCDKeyError(key)

    def _build_keys(self) -> List[str]:
        keys_list = []
        for key in self.__dict__:
            if key in self:
                keys_list.append(key)

        return keys_list

    # mapping methods ----------------------------------------------------------
    def __iter__(self):
        self._current_index = -1
        self._keys_cache = self._build_keys()
        yield from self._keys_cache

    def __next__(self):
        self._current_index += 1
        if self._current_index < len(self._keys_cache):
            return self._keys_cache[self._current_index]
        raise StopIteration()

    def __getitem__(self, key: Union[str, int]) -> Any:
        if isinstance(key, int) and key < len(self):
            return list(self.values())[key]
        return self._in_fields(key)

    def __setitem__(self, key: str, value: Any):
        self._set_field(key, value)

    def __len__(self) -> int:
        return len(self.__dict__) - 3

    def __delitem__(self, key: str) -> Any:
        if key in self:
            del self.__dataclass_fields__[key]
            del self.__annotations__[key]
            return self.__dict__.pop(key)
        raise PCDKeyError(key)

    def __contains__(self, key: str):
        return (key not in ["dataclass_instanced", "_current_index",
                            "_keys_cache"] and key in self.__dict__)

    def values(self):
        for key in self:
            yield self[key]

    def items(self):
        for key in self:
            yield key, self[key]

    def clear(self):
        while True:
            try:
                del self[next(self)]
            except StopIteration:
                break

    pop = __delitem__
    keys = __iter__

    # creation helpers ---------------------------------------------------------
    @staticmethod
    def _get_core(core_name: str) -> 'panda_core_data.DataCore':
        from . import data_core

        if isinstance(data_core, dict) and not core_name:
            return data_core["DEFAULT"]

        if isinstance(data_core, dict) and core_name:
            return data_core[core_name]

        # This return statement is necessary, however, for some reason the
        # coverage doesn't detect it
        return data_core  # pragma: no cover

    @staticmethod
    def _add_into(data_type: 'DataType', data_type_dict, **kwargs):
        """You can use the prefix `dataclass_` with a dataclass parameter to
        configure it. They can be found in this link:
        https://docs.python.org/3/library/dataclasses.html#dataclasses.dataclass

        For example:

        .. code:: python

            from panda_core_data.model import Model

            class ModelName(Model, dataclass_init=False):
                out: int

                def __init__(self, num):
                    self.out = num ** num

        Will make the library not create a `__init__` method and use yours
        instead.

        :param data_type: class type to be added
        :param template_name: The name of the template, if not supplied, the
                              class name is used.
        :type template_name: None or str
        :param dependency_list: :class:`Template` to be used as dependency.
        :type dependency_list: list[str]"""
        from .data_core_bases import GroupWrapper

        if not hasattr(data_type, "dataclass_args"):
            generate_dataclass_args(data_type, **kwargs)
            data_type = _process_class(data_type, **data_type.dataclass_args)

            def new_init(self, *init_args, db_file: Optional[str] = None,
                         default_table: str = DataType.DEFAULT_TABLE,
                         **init_kwargs):
                from .model import Model
                if db_file:
                    self.load_db(db_file, *init_args,
                                 default_table=default_table, **init_kwargs)
                elif self.original_init:
                    self.original_init(*init_args, **init_kwargs)

                if isinstance(self, Model):
                    self.wrapper.instances.append(self)
                else:
                    self.wrapper.instances = self

                if hasattr(self, "__post_init__"):
                    self.__post_init__(*init_args, **init_kwargs)

            if(hasattr(data_type, "__init__") and
               data_type.__init__ is not new_init):
                if data_type.__init__ is not TinyDB.__init__:
                    data_type.original_init = data_type.__init__

                data_type.__init__ = new_init

        replace = kwargs.pop("replace", False)
        data_name = kwargs.pop("data_name", data_type.__name__)
        data_type.dependencies = kwargs.pop("dependencies", [])

        data_type.data_name = data_name
        data_type.data_type_dict = data_type_dict
        data_type.wrapper = GroupWrapper(data_type)

        if data_name not in data_type_dict or replace:
            data_type_dict[data_name] = data_type
        else:
            raise PCDDuplicatedTypeName(
                f"There's already a {type(data_type)} with the name "
                f"{data_name}")

    @property
    def has_dependencies(self) -> bool:
        """If the model has any dependencies

        :return: If the instance have dependencies or not."""
        check_if_valid_instance(self, DataType)
        return any(self.dependencies)

    # def load_inner_dependencies(self, dependency):
    #    check_if_valid_instance(dependency, DataType)
    #
    #    tmp_dependencies = {dependency.data_name: dependency}
    #
    #    for current_data in dependency.parents.values():
    #        tmp_dependencies.update(self.load_inner_dependencies(current_data))
    #
    #    return tmp_dependencies

    @property
    def is_instanced(self) -> bool:
        return isinstance(self, type(self))

    @classmethod
    def instance_from_raw(cls, raw_file) -> 'DataType':
        return cls(db_file=raw_file)

    def load_db(self, db_file: PathType, *init_args,
                default_table: str = DEFAULT_TABLE, **kwargs):
        """Method that load raw files and assign each field to an attribute.

        :param db_file: Path to a raw file
        :param tinydb.storages.Storage storage: storage class to be used.
        :param default_table: default main field in the raw file."""
        check_if_valid_instance(self, DataType)

        db_file = auto_convert_to_pathlib(db_file)
        extension = get_extension(db_file)
        storage = get_storage_from_extension(extension)

        TinyDB.__init__(self, db_file, *init_args, storage=storage,
                        default_table=default_table, **kwargs)

        for current_field in self.all():
            setattr(self, list(current_field.keys())[0],
                    list(current_field.values())[0])

    def all(self, *arg, **kwargs):
        return self._table.all(*arg, **kwargs)

    def add_dependencies(self):
        "Add all dependencies for the model"
        for current_dependency in self.dependencies:
            dependency = self.data_core.get_template_type(current_dependency)
            dependency = dependency.instanced()
            # if dependency.has_dependencies:
            #    self.parents.update(self.load_inner_dependencies(dependency))

            self.parents[current_dependency] = dependency

    # context methods ----------------------------------------------------------
    def save_to_file(self, *_):
        "Save fields instance into the raw"
        to_write = {self.DEFAULT_TABLE: []}
        for the_field in fields(self):
            to_write[self.DEFAULT_TABLE].append(
                {the_field.name: getattr(self, the_field.name)})

        self._storage.write(to_write)
        self.close()

    __exit__ = save_to_file

    #===========================================================================
    # def get(self, *arg, **kwargs):
    #     return self._table.get(*arg, **kwargs)
    #===========================================================================

    #===========================================================================
    # def purge(self, *arg, **kwargs):
    #     return self._table.purge(*arg, **kwargs)
    #===========================================================================

    #===========================================================================
    # def insert_multiple(self, *arg, **kwargs):
    #     return self._table.insert_multiple(*arg, **kwargs)
    #===========================================================================


def generate_dataclass_args(data_type: DataType, **kwargs):
    """Extract dataclass arguments from the :class:`DataType`

    :param data_type: The :class:`DataType`"""
    data_type.dataclass_args = {}

    if "dataclass_repr" in kwargs:  # pragma: no cover
        PCDTypeError("'repr' is always False with Data Types")

    # Let's extract the dataclass parameters from kwarg
    for param_name, param in signature(dataclass).parameters.items():
        # We use a custom repr for our Data Types.
        if param_name == "repr":
            data_type.dataclass_args[param_name] = False

        # both cls and _cls are to avoid bugs with nightly version of python.
        elif param_name not in ["_cls", "cls"]:
            dt_param_name = "dataclass_" + param_name
            data_type.dataclass_args[param_name] = kwargs.pop(dt_param_name,
                                                              param.default)
