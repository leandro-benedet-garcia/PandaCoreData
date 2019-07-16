"""
Module that deals with parsing yaml files using pyyaml
"""

from tinydb.database import Document
from tinydb.storages import Storage, MemoryStorage
import yaml


class YAMLStorage(MemoryStorage, Storage):
    """
    Parser storage class used to read yaml files
    """
    def __init__(self, path):
        """
        Open file as Data Base

        :param path: path pointing to a yaml file
        :type path: str
        """
        super().__init__()
        self.path = path
        yaml.add_representer(Document, self.represent_doc)

    def read(self):
        """
        Method used by TinyDB to read the file
        """
        if not self.memory:
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
        """
        Method used to transform a dict to a yaml repreentation

        :param dumper: yaml dumper
        :param data: data to be parsed
        """
        return dumper.represent_data(dict(data))
