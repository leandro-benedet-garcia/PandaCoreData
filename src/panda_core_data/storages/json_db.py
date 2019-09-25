from tinydb.storages import JSONStorage

#pylint: disable=unused-import
import panda_core_data

from .base_db import BaseDB


class JsonDB(BaseDB):
    extensions = ["json", ]

    def read(self) -> 'panda_core_data.DataDict':
        return self.base_read(JSONStorage.read, False)

    def write(self, data):
        self.base_write(JSONStorage.write, data, False)
