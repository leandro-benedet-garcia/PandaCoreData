'''
Created on 2019-04-30

@author: Leandro (Cerberus1746) Benedet Garcia
'''

import os.path

from tinydb import TinyDB

from core_data import yaml_db
from tinydb.queries import Query
from logger import log_debug

class ModelMixin(TinyDB):
	"""
	Base for all the model types, be it template or model
	"""

	DEFAULT_TABLE = 'data'
	DEFAULT_STORAGE = yaml_db.YAMLStorage

	"""def __init__(self, mod, db_file=False, load_db=True):
		'''
		:param mod: mod that owns the model
		:type mod: Mod
		:param db_file: yaml file path
		:type db_file: string
		'''
		if load_db and not db_file:
			raise AttributeError("db_file attribute must be set if load_db is true")

		if load_db:
			log_debug(f"Loading DB file <b>{db_file}</b>")
			if not os.path.isfile(db_file):
				raise FileNotFoundError("File {} don't exist".format(db_file))
			try:
				super().__init__(db_file, storage=self.DEFAULT_STORAGE, default_table=self.DEFAULT_TABLE)
				log_debug(f"DB file <b>{db_file}</b> loaded succesfully")
			except ValueError as ex:
				additional_info = "Error in file {}\n".format(db_file)
				additional_info = '{}: {}'.format(additional_info, ex.args[0]) if ex.args else str(db_file)
				ex.args = (additional_info,) + ex.args[1:]
				raise

		self.parents = {}
		self.mod = mod
		self.core = mod.core
		self.load_db = load_db

		self.query = Query()

		if self.has_dependencies:
			self.add_dependencies()"""

	def __getattr__(self, name):
		try:
			return self.__dict__[name]
		except KeyError:
			raise AttributeError("{} object has no attribute {}".format(type(self), name))

	def __setattr__(self, attr_name, value):
		self.__dict__[attr_name] = value

	@property
	def has_dependencies(self):
		"""If the model has any dependencies"""
		return len(self.dependency_list) > 0

	@property
	def model_name(self):
		"""get the model name"""
		if not hasattr(self, "_model_name"):
			current_type = type(self)
			type_name = current_type.__name__.lower()
			type_name = type_name.replace("model", "").replace("template", "")
			self._model_name = str(type_name)

		return self._model_name

	@staticmethod
	def load_inner_dependencies(dependency):
		tmp_dependencies = {dependency.model_name: dependency}

		for current_data in dependency.parents.values():
			tmp_dependencies.update(ModelMixin.load_inner_dependencies(current_data))

		return tmp_dependencies

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
			return False

	def add_dependencies(self):
		"""Add a dependency to the model"""
		for current_dependency in self.dependency_list:
			log_debug(f"Loading dependency: <b>{current_dependency}</b> for {self.model_name}")
			dependency = self.mod.loaded_model_template.get(current_dependency, False)
			if dependency.has_dependencies:
				self.parents.update(self.load_inner_dependencies(dependency))

			if not dependency:
				raise ImportError("Dependency {} not found for {}".format(current_dependency, self.name))
			self.parents[current_dependency] = dependency