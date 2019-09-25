from tinydb.storages import JSONStorage

from ..custom_typings import DataDict
from .base_db import BaseDB


class JsonDB(BaseDB):
    extensions = ["json", ]

    def read(self) -> DataDict:
        return self.base_read(JSONStorage.read, False)

    def write(self, data):
        self.base_write(JSONStorage.write, data, False)
