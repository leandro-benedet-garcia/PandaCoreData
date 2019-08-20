from tinydb.storages import JSONStorage
from .base_db import BaseDB

class JsonDB(BaseDB):
    extensions = ["json",]

    def read(self):
        return self.base_read(JSONStorage.read, False)

    def write(self, data):
        self.base_write(JSONStorage.write, data, False)
