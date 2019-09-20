'''
This is the heart of Models and Templates

:created: 2019-04-30
:author: Leandro (Cerberus1746) Benedet Garcia
'''
from inspect import signature
from dataclasses import dataclass, _process_class, fields

from tinydb import TinyDB
from tinydb.queries import Query

from .storages import auto_convert_to_pathlib, get_storage_from_extension, get_extension
from .custom_exceptions import PCDDuplicatedTypeName, PCDTypeError
from .utils import check_if_valid_instance


class DataType(TinyDB):
    """
    Base for all the model types, be it template or model

    Internally it uses the TinyDB database
    """
    DEFAULT_TABLE = 'data'
    parents = {}
    query = Query()
    raws = []

    data_name: str
    dependencies: list
    data_group: "Group"
    data_core: "DataCore"
    wrapper: "GroupWrapper"

    def __new__(cls, *_, db_file=False, **__):
        """
        Method that handles the instancing of the models and templates, this is necessary because
        dataclasses create a custom __init__ method. Which we doesn't use at all if a raw file is
        supplied.

        :param cls: the type to be instanced
        :type cls: Model or Template
        :param str path: path to the raw file to be loaded, if False, the class will be instanced
                         like a normal dataclass
        """
        from .model import Model

        if not hasattr(cls, "original_init"):
            cls.original_init = None

        if cls.dataclass_args['init'] and cls.original_init is None:
            def with_old_init(self, *init_args, db_file=None, default_table=DataType.DEFAULT_TABLE,
                              **init_kwargs):

                if db_file:
                    self.load_db(db_file, *init_args, default_table=default_table, **init_kwargs)
                elif self.original_init is not None:
                    self.original_init(*init_args, **init_kwargs)

                if isinstance(self, Model):
                    self.wrapper.instances.append(instanced)
                else:
                    self.wrapper.instances = instanced


                if hasattr(self, "__post_init__"):
                    return self.__post_init__(*init_args, **init_kwargs)

            #pylint: disable=comparison-with-callable
            if hasattr(cls, "__init__") and cls.__init__ != with_old_init:
                cls.original_init = cls.__init__
                cls.__init__ = with_old_init

        instanced = object.__new__(cls)

        instanced.dataclass_instanced = not isinstance(db_file, str)

        return instanced

    def __getattr__(self, attr_name):
        """
        This is here just to make this method back to the default that was overwritten by TinyDB

        :param str name: name of the attribute to get
        """
        raise AttributeError(f"type object '{type(self).__name__}' has no attribute '{attr_name}'")

    def __setattr__(self, attr_name, value):
        """
        This is here just to make this method back to the default that was overwritten by TinyDB

        :param str name: name of the attribute to write
        :param any value: value of the attribute.
        """
        object.__setattr__(self, attr_name, value)

    def __repr__(self):
        return_value = []
        if self.data_name != type(self).__name__:
            return_value.append(f"DataType {self.data_name} ({type(self).__name__}):")
        else:
            return_value.append(f"DataType {self.data_name}:")
        return_value.append("\tFields:")
        fields_list = [
            f"\t\t{current_field.name}({current_field.type}) = {getattr(self, current_field.name)}"
            for current_field in fields(self)
        ]
        return_value.append('\n'.join(fields_list))

        #if any(self.parents):
        #    checked_parents = [self.data_name,]
        #    return_value.append("\tParents:")
        #    for parent_name, parent_value in self.parents.items():
        #        if parent_name in checked_parents:
        #            continue
        #        checked_parents.append(parent_name)
        #        return_value.append("\t\t" + parent_name + "\n\t\t\t" +
        #                            repr(parent_value).replace("\n", "\n\t\t\t"))

        return "\n".join(return_value)

    @staticmethod
    def _get_core(core_name):
        from . import data_core

        if isinstance(data_core, dict) and not core_name:
            return data_core["DEFAULT"]

        if isinstance(data_core, dict) and core_name:
            return data_core[core_name]

        # This return statement is necessary, however, for some reason the coverage doesn't detect
        # it
        return data_core # pragma: no cover

    @staticmethod
    def _add_into(data_type, data_type_dict, **kwargs):
        """
        You can use the prefix `dataclass_` with a dataclass parameter to configure it. They can be
        found in this link:
        https://docs.python.org/3/library/dataclasses.html#dataclasses.dataclass

        For example:

        .. code:: python

            from panda_core_data.model import Model

            class ModelName(Model, dataclass_init=False):
                out: int

                def __init__(self, num):
                    self.out = num ** num

        Will make the library not create a `__init__` method and use yours instead.

        :param cls: class type to be added
        :type cls: Model or Template
        :param str template_name: The name of the template, if not supplied, the class name is used.
        :param dependency_list: :class:`Template` to be used as dependency.
        :type dependency_list: list(str)
        """
        from .data_core_bases import GroupWrapper
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
                data_type.dataclass_args[param_name] = kwargs.pop("dataclass_" + param_name,
                                                                  param.default)

        data_type = _process_class(data_type, **data_type.dataclass_args)

        replace = kwargs.pop("replace", False)
        data_name = kwargs.pop("data_name", data_type.__name__)
        data_type.dependencies = kwargs.pop("dependencies", [])

        data_type.data_name = data_name
        data_type.data_type_dict = data_type_dict
        data_type.wrapper = GroupWrapper(data_type)

        if data_name not in data_type_dict or replace:
            data_type_dict[data_name] = data_type
        else:
            raise PCDDuplicatedTypeName(f"There's already a {type(data_type)} with the name "
                                        f"{data_name}")

    @property
    def has_dependencies(self):
        """
        If the model has any dependencies

        :return bool: If the instance have dependencies or not.
        """
        check_if_valid_instance(self, DataType)
        return any(self.dependencies)

    #def load_inner_dependencies(self, dependency):
    #    check_if_valid_instance(dependency, DataType)
    #
    #    tmp_dependencies = {dependency.data_name: dependency}
    #
    #    for current_data in dependency.parents.values():
    #        tmp_dependencies.update(self.load_inner_dependencies(current_data))
    #
    #    return tmp_dependencies

    @classmethod
    def instance_from_raw(cls, raw_file):
        return cls(db_file=raw_file)

    def load_db(self, db_file, *init_args, default_table=DEFAULT_TABLE, **kwargs):
        """
        Method that load raw files and assign each field to an attribute.

        :param str db_file: Path to a raw file
        :param tinydb.storages.Storage storage: storage class to be used, it needs to inherit
                                                :class:`~tinydb.storages.Storage`
        :param str default_table: default main field in the raw file.
        """
        check_if_valid_instance(self, DataType)

        db_file = auto_convert_to_pathlib(db_file)
        extension = get_extension(db_file)
        storage = get_storage_from_extension(extension)

        TinyDB.__init__(self, db_file, *init_args, storage=storage, default_table=default_table,
                        **kwargs)

        for current_field in self.all():
            setattr(self, list(current_field.keys())[0], list(current_field.values())[0])

    def all(self, *arg, **kwargs):
        return self._table.all(*arg, **kwargs)

    def add_dependencies(self):
        """Add all dependencies for the model"""
        for current_dependency in self.dependencies:
            dependency = self.data_core.get_template_type(current_dependency)
            dependency = dependency.instanced()
            #if dependency.has_dependencies:
            #    self.parents.update(self.load_inner_dependencies(dependency))

            self.parents[current_dependency] = dependency

    def save_to_file(self):
        """Save fields instance into the raw"""
        to_write = {self.DEFAULT_TABLE: []}
        for the_field in fields(self):
            to_write[self.DEFAULT_TABLE].append({the_field.name: getattr(self, the_field.name)})

        self._storage.write(to_write)

    #===============================================================================================
    # def get(self, *arg, **kwargs):
    #     return self._table.get(*arg, **kwargs)
    #===============================================================================================

    #===============================================================================================
    # def purge(self, *arg, **kwargs):
    #     return self._table.purge(*arg, **kwargs)
    #===============================================================================================

    #===============================================================================================
    # def insert_multiple(self, *arg, **kwargs):
    #     return self._table.insert_multiple(*arg, **kwargs)
    #===============================================================================================
