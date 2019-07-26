'''
This is the heart of Models and ModelTemplates

:created: 2019-04-30
:author: Leandro (Cerberus1746) Benedet Garcia
'''
import os
from inspect import signature
from dataclasses import dataclass, _process_class

from tinydb import TinyDB
from tinydb.queries import Query

from .yaml_db import YAMLStorage
from .custom_exceptions import PCDDuplicatedTypeName


class ModelMixin(TinyDB):
    """
    Base for all the model types, be it template or model

    Internally it uses the TinyDB database
    """

    DEFAULT_TABLE = 'data'
    DEFAULT_STORAGE = YAMLStorage
    parents = {}
    query = Query()

    data_name: str
    dependencies: list
    data_group: "Group"
    data_core: "DataCore"
    wrapper: "GroupWrapper"
    all_data_instances: "Group"

    def __new__(cls, *_, db_file=False, **__):
        """
        Method that handles the instancing of the models and templates, this is necessary because
        dataclasses create a custom __init__ method. Which we doesn't use at all if a raw file is
        supplied.

        :param cls: the type to be instanced
        :type cls: class that inherits from Model or ModelTemplate.
        :param path: path to the raw file to be loaded, if False, the class will be instanced \
        like a normal dataclass
        :type path: str
        """
        if db_file:
            # TODO: Find a way to not overwrite init if the user creates one
            def custom_init(self, db_file, *init_args, storage=ModelMixin.DEFAULT_STORAGE,
                            default_table=ModelMixin.DEFAULT_TABLE, **init_kwargs):

                self.load_db(db_file, *init_args, storage=storage, default_table=default_table,
                             **init_kwargs)

                if hasattr(self, "__post_init__"):
                    return self.__post_init__(*init_args, **init_kwargs)

            cls.__init__ = custom_init

        instanced = object.__new__(cls)

        instanced.dataclass_instanced = not isinstance(db_file, str)
        instanced.database_instanced = not instanced.dataclass_instanced

        return instanced

    def __getattr__(self, name):
        """
        This is here just to make this method back to the default that was overwritten by TinyDB

        :param name: name of the attribute to get
        :type name: str
        """
        raise AttributeError(f"type object has no attribute '{name}'")

    def __setattr__(self, attr_name, value):
        """
        This is here just to make this method back to the default that was overwritten by TinyDB

        :param name: name of the attribute to write
        :type name: str
        :param value: value of the attribute.
        """
        object.__setattr__(self, attr_name, value)

    def __repr__(self):
        fields = [f"{field_name}({field_type}) = {getattr(self, field_name)}"
                  for field_name, field_type in self.__annotations__.items()]
        return "Group: \n" + ', '.join(fields) + "\n" + super().__repr__()

    @staticmethod
    def _add_into(data_type, data_type_dict, add_method, *args, **kwargs):
        from . import data_core

        dataclass_args = {}
        # Let's extract the dataclass parameters from kwarg
        for param_name, param in signature(dataclass).parameters.items():
            # If we load attrs from the file, we will never use the dataclass init
            if param_name == "repr":
                dataclass_args[param_name] = False

            # both cls and _cls are to avoid bugs with nightly version of python.
            elif param_name not in ["_cls", "cls"]:
                dataclass_args[param_name] = kwargs.pop(param_name, param.default)

        data_type = _process_class(data_type, **dataclass_args)

        group_name = kwargs.pop("group_name", "DEFAULT_DATA_GROUP")
        replace = kwargs.get("replace", False)
        data_name = kwargs.pop("data_name", data_type.__name__)

        data_type.data_name = data_name
        data_type.dependencies = kwargs.pop("dependencies", [])
        data_type.data_core = data_core
        data_type.data_type_dict = data_type_dict

        if data_name not in data_type_dict or replace:
            data_type_dict[data_name] = data_type
        else:
            raise PCDDuplicatedTypeName(f"There's already a {type(data_type)} with the name "
                                        f"{data_name}")

        add_method(group_name, data_type, *args, **kwargs)


    @property
    def has_dependencies(self):
        """If the model has any dependencies"""
        return any(self.dependencies)

    @classmethod
    def all_instances(cls):
        return cls.wrapper.instances

    @staticmethod
    def load_inner_dependencies(dependency):
        tmp_dependencies = {dependency.data_name: dependency}

        for current_data in dependency.parents.values():
            tmp_dependencies.update(ModelMixin.load_inner_dependencies(current_data))

        return tmp_dependencies

    @classmethod
    def instance_from_raw(cls, raw_file):
        return cls(db_file=raw_file)

    def load_db(self, db_file, *init_args, storage=DEFAULT_STORAGE, default_table=DEFAULT_TABLE,
                **init_kwargs):
        """
        Method that load raw files and assign each field to an attribute.

        :param db_file: Path to a raw file
        :type db_file: str
        :param storage: storage class to be used, it needs to inherit TinyDB.tinydb.storages.Storage
        :type storage: TinyDB.tinydb.storages.Storage
        :param default_table: default main field in the raw file.
        :type default_table: str
        """
        if not os.path.isfile(db_file):
            raise FileNotFoundError(f"File '{db_file}' don't exist")

        TinyDB.__init__(self, db_file, *init_args, storage=storage,
                        default_table=default_table, **init_kwargs)

        for current_field in self.all():
            setattr(self, list(current_field.keys())[0], list(current_field.values())[0])

    def get(self, *arg, **kwargs):
        return self._table.get(*arg, **kwargs)

    def all(self, *arg, **kwargs):
        return self._table.all(*arg, **kwargs)

    def purge(self, *arg, **kwargs):
        return self._table.purge(*arg, **kwargs)

    def insert_multiple(self, *arg, **kwargs):
        return self._table.insert_multiple(*arg, **kwargs)

    def add_dependencies(self):
        """Add a dependency to the model"""
        for current_dependency in self.dependencies:
            dependency = self.data_core.get_template_from_all(current_dependency)
            dependency = dependency.all_data_instances[0]
            if dependency.has_dependencies:
                self.parents.update(self.load_inner_dependencies(dependency))

            self.parents[current_dependency] = dependency
