from tinydb.storages import MemoryStorage, JSONStorage

from ..custom_exceptions import PCDInvalidRaw


#pylint: disable=invalid-name
available_storages = []

class BaseDB(JSONStorage, MemoryStorage):
    """
    Base storage class that reads which extensions are available to feed the path handling functions
    """
    extensions = False

    def __init_subclass__(cls):  # @NoSelf
        available_storages.append({
            "name": cls.__name__,
            "extensions": cls.extensions,
            "storage": cls,
        })

    def __init__(self, path, **kwargs):
        self.path = path
        MemoryStorage.__init__(self)
        JSONStorage.__init__(self, path, **kwargs)

    def base_read(self, load_method, use_handle):
        """Base method used by children classes to read the file"""
        if not self.memory:
            if use_handle:
                data = load_method(self._handle.read())
            else:
                data = load_method(self)

            if not any(data):
                raise PCDInvalidRaw(f"the raw {self.path} is invalid or empty")

            desired_data = {}
            for table, table_items in data.items():
                desired_data[table] = {}
                for item_index, current_item in enumerate(table_items):
                    desired_data[table][item_index] = current_item
            self.memory = desired_data

        return self.memory

    def base_write(self, data):
        MemoryStorage.write(self, data)
