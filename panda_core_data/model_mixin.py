'''
Created on 2019-04-30

:author: Leandro (Cerberus1746) Benedet Garcia
'''
import os
from tinydb import TinyDB

from .yaml_db import YAMLStorage
from tinydb.queries import Query

from inspect import signature
from dataclasses import dataclass, _process_class

class ModelMixin(TinyDB):
	"""
	Base for all the model types, be it template or model

	Internally it uses the TinyDB database
	"""

	DEFAULT_TABLE = 'data'
	DEFAULT_STORAGE = YAMLStorage
	parents = {}
	query = Query()

	def __new__(cls, *args, db_file=False, **kwargs):
		"""
		Method that handles the instancing of the models and templates, this is necessary because
		dataclasses create a custom __init__ method. Which we doesn't use at all if a raw file is
		supplied.

		:param cls: the type to be instanced
		:type cls: class that inherits from Model or ModelTemplate.
		:param path: path to the raw file to be loaded, if False, the class will be instanced
		like a normal dataclass
		:type path: str
		"""
		dataclass_args = {}
		#Let's extract the dataclass parameters from kwarg
		for param_name, param in signature(dataclass).parameters.items():
			#If we load attrs from the file, we will never use the dataclass init
			if db_file and param_name == "init":
				dataclass_args[param_name] = False
				kwargs.pop("init", None)
				continue

			# both cls and _cls are to avoid bugs with nightly version of python.
			if param_name not in ["_cls", "cls"]:
				dataclass_args[param_name] = kwargs.pop(param_name, param.default)

		cls = _process_class(cls, **dataclass_args)

		if db_file:
			def custom_init(self, db_file, *init_args, storage=ModelMixin.DEFAULT_STORAGE,
				default_table=ModelMixin.DEFAULT_TABLE, **init_kwargs):

				self.load_db(db_file, *init_args, storage=storage, default_table=default_table,
					**init_kwargs)

				if hasattr(self, "__post_init__"):
					return self.__post_init__(db_file, *init_args, storage=ModelMixin.DEFAULT_STORAGE,
						default_table=ModelMixin.DEFAULT_TABLE, **init_kwargs)

			cls.__init__ = custom_init

		instanced = object.__new__(cls)

		instanced.dataclass_instanced = type(db_file) != str
		instanced.database_instanced = not instanced.dataclass_instanced

		return instanced

	def __getattr__(self, name):
		raise AttributeError(f"type object '{self}' has no attribute '{name}'")

	def __setattr__(self, attr_name, value):
		object.__setattr__(self, attr_name, value)

	@property
	def has_dependencies(self):
		"""If the model has any dependencies"""
		return len(self.dependencies) > 0

	@staticmethod
	def load_inner_dependencies(dependency):
		tmp_dependencies = {dependency.model_name: dependency}

		for current_data in dependency.parents.values():
			tmp_dependencies.update(ModelMixin.load_inner_dependencies(current_data))

		return tmp_dependencies

	def load_db(self, db_file, *init_args, storage=DEFAULT_STORAGE, default_table=DEFAULT_TABLE,
			**init_kwargs):
		if type(db_file) != str:
			raise TypeError(f"db_file has to be a str {type(db_file)} found instead.")

		if not os.path.isfile(db_file):
			raise FileNotFoundError(f"File {db_file} don't exist")
		try:
			TinyDB.__init__(self, db_file, *init_args, storage=storage,
				default_table=default_table, **init_kwargs)

			for current_field in self.all():
				setattr(self, list(current_field.keys())[0], list(current_field.values())[0])

		except ValueError as ex:
			additional_info = f"Error in file {db_file}\n"
			additional_info = '{}: {}'.format(additional_info,
				ex.args[0]) if ex.args else str(db_file)
			ex.args = (additional_info,) + ex.args[1:]
			raise

	def get(self, *arg, **kwargs):
		return self._table.get(*arg, **kwargs)

	def all(self, *arg, **kwargs):
		return self._table.all(*arg, **kwargs)

	def purge(self, *arg, **kwargs):
		return self._table.purge(*arg, **kwargs)

	def insert_multiple(self, *arg, **kwargs):
		return self._table.insert_multiple(*arg, **kwargs)

	def get_single_value(self, field_name):
		current_query = self.query[field_name]
		condition = current_query.exists()
		current_row = self.get(condition)
		if current_row:
			return current_row[field_name]
		else:
			raise AttributeError