DEFAULT_MODEL_GROUP = "DEFAULT_MODEL_GROUP"
'''Default model group name, used for types and instances.'''

DEFAULT_TEMPLATE_GROUP = "DEFAULT_TEMPLATE_GROUP"
'''Default template group name, used for types and instances.'''

from .custom_exceptions import *
from os.path import isdir

class DataCore(object):
	"""
	Class where everything is kept.
	"""
	all_model_types = {}
	all_template_types = {}
	raw_folders = []

	def add_raw_folder(self, folder: str):
		"""
		Add folder to the raws search path.

		:param folder: folder to be added.
		:type folder: str
		"""
		if not isdir(folder):
			raise FolderNotFound(f"The folder {folder} doesn't exist.")
		self.raw_folders.append(folder)

	def get_or_create_model_type_group(self, name: str):
		"""
		Get a group of model types, if it doesn't exist, the group is created.

		:param name: name of the group
		:type name: string
		"""
		return self.all_model_types.setdefault(name, {})

	def add_model_type_to_group(self, group_name: str, model, auto_create_group=True):
		"""
		Add a model type to a group.

		If auto_create_group is true and the group doesn't exist it will be created.
		If false an exception will be raised.

		:param group_name: Name of the group
		:type group_name: str
		:param model: Model to be added
		:type model: Model
		:param auto_create_group: If the group should be created if it doesn't exist
		:type auto_create_group: bool
		:raises DuplicatedModelTypeName: If there's a model with the supplied name inside the group
		"""
		if auto_create_group:
			group = self.get_or_create_model_type_group(group_name)
		else:
			group = self.get_model_type_group(group_name)

		model_name = model.model_name

		if model_name in group:
			raise DuplicatedModelTypeName(f"There's already a model type with "
				f"the name {model_name} inside the group {group_name}")
		else:
			group[model_name] = model

	def get_model_type_group(self, name: str, default=None):
		"""
		Get model. It will raise an exception if the group doesn't exist.

		:param name: The name of the group
		:type name: str
		:param default: Default value to be returned if model type is not found, if none, it will
		raise an exception, which is the default.
		:type default: any
		:raises ModelTypeGroupNotFound: If the group doesn't exist.
		"""
		group = self.all_model_types.get(name, default)
		if not group and default == None:
			raise ModelTypeGroupNotFound(f"Group {name} wasn't found.")

		return group

	def get_model_type(self, name: str, group_name: str=DEFAULT_MODEL_GROUP, default=None):
		"""
		Get model type from the group

		:param name: Name of the model type to get
		:type name: str
		:param group: Name of the group
		:type group: str
		:param default: Default value to be returned if model type is not found, if none, it will
		raise an exception, which is the default.
		:type default: any
		:raises ModelTypeNotFound: If the model doesn't exist.
		"""
		group = self.get_model_type_group(group_name, default=False)
		if group:
			model = group.get(name, default)
			if not model and default == None:
				raise ModelTypeNotFound(f"Model type {name} could not be found inside "
					f"the group {group_name}")
		else:
			return default
		return model

	def get_or_create_template_group(self, name: str):
		pass

data_core = DataCore()