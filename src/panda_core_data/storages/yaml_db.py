"""Module that deals with parsing yaml files using pyyaml"""
from tinydb.database import Document
import yaml
from .base_db import BaseDB


class YamlDB(BaseDB):
    """Parser storage class used to read yaml files"""
    extensions = ["yaml", "yml"]

    def __init__(self, *args, **kwargs):
        """
        Open file as Data Base

        :param path str: path pointing to a yaml file
        """
        super().__init__(*args, **kwargs)
        yaml.add_representer(Document, lambda dumper, data: dumper.represent_data(dict(data)))

    def read(self):
        """Method used by TinyDB to read the file"""
        return self.base_read(yaml.safe_load, True)

    def write(self, data):
        self.base_write(yaml.dump, data, True)
