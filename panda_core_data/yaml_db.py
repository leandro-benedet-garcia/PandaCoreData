from tinydb.database import Document
from tinydb.storages import Storage, MemoryStorage
import yaml


class YAMLStorage(MemoryStorage, Storage):
	def __init__(self, path):
		super().__init__()
		self.path = path
		yaml.add_representer(Document, self.represent_doc)
		self.first_read = True

	def read(self):
		if not self.memory:
			self.first_read = False
			with open(self.path) as handle:
				data = yaml.safe_load(handle.read())
				if data:
					desired_data = {}
					for table, table_items in data.items():
						desired_data[table] = {}
						for item_index, current_item in enumerate(table_items):
							desired_data[table][item_index] = current_item
					self.memory = desired_data
				else:
					self.memory = None

		return self.memory


	@staticmethod
	def represent_doc(dumper, data):
		return dumper.represent_data(dict(data))
