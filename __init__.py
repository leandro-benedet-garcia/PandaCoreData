DEFAULT_MODEL_GROUP = "_default_models"
DEFAULT_TEMPLATE_GROUP = "_default_templates"

class DataCore(object):
	all_model_types = {}
	all_templates = {}

	def get_or_create_model_group(self, name: str):
		return self.all_model_types.setdefault(name, {})

	def add_model_type_to_group(self, group_name: str, model):
		group = self.get_or_create_model_group(group_name)
		model_name = model.model_name
		if model_name in group:
			raise Exception()
		else:
			group[model_name] = model

	def get_or_create_template_group(self, name: str):
		pass

data_core = DataCore()
