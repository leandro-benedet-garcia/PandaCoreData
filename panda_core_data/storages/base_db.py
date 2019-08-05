import os
from tinydb.storages import MemoryStorage, JSONStorage


#pylint: disable=invalid-name
available_storages = []

class BaseDB(JSONStorage, MemoryStorage):
    """
    Base storage class that reads which extensions are available to feed the path handling functions

    To create a new storage, you will need to inherit this class, create a `extensions` variable
    containing a list of extensions the storage will support for example:

    .. code:: python

            extensions = ["yml", "yaml"]

    then implement a `read` and `write` method using the methods
    :meth:`~panda_core_data.storages.base_db.BaseDB.base_read` and
    :meth:`~panda_core_data.storages.base_db.BaseDB.base_write` all you need to do is follow the
    instructions contained in them
    """
    extensions = False

    def __init_subclass__(cls):  # @NoSelf
        """
        Automatically generate an extension list containing the available raw extensions available
        together with their storage.
        """
        available_storages.append({
            "name": cls.__name__,
            "extensions": cls.extensions,
            "storage": cls,
        })

    def __init__(self, path, **kwargs):
        """
        Create a new instance.

        :param str path: Path to file
        """
        self.path = path
        MemoryStorage.__init__(self)
        JSONStorage.__init__(self, path, **kwargs)

    def base_read(self, load_method, use_handle):
        """
        Base method used by children classes to read the file and transforms the string into a
        list of dictionaries, a good example of this method is the built in python
        :func:`json.load` however, since it needs a string as an input (or handler) you would need
        to set the parameter use_handler so the string, which is the contents of the raw file, will
        be passed to that method. For example the read method of our yaml parser:

        .. code:: python

            def read(self):
                return self.base_read(yaml.safe_load, True)

        And since the function :func:`yaml.safe_load` needs a string as an input, we set use_handle
        to True.

        An example of list of dictionaries would be like this:

        .. code:: python

            {"data": [
                {
                    'field_name': 'value',
                    'another_field': 10,
                },
                {
                    'field_name': 'value',
                    'another_field': 10,
                },
            ]}

        The dict keys are fields of a :mod:`~dataclasses.dataclass` and the value, well, values.

        :param load_method: method used to transform the raw file into a list of dictionaries.
        :type load_method: :class:`function`
        :param bool use_handle: TinyDB offers a handle (More specifically, the handle of the class
                                :class:`~tinydb.storages.JSONStorage`) to load the file and turn
                                into a string automatically if you'd like to use it, just set this
                                parameter to True.
        """
        if not self.memory:
            if use_handle:
                data = load_method(self._handle.read())
            else:
                data = load_method(self)

            desired_data = {}
            for table, table_items in data.items():
                desired_data[table] = {}
                for item_index, current_item in enumerate(table_items):
                    desired_data[table][item_index] = current_item
            self.memory = desired_data

        return self.memory

    def base_write(self, write_method, data, use_handle):
        """
        Transforms the data dictionary to a raw representation.

        :param data: data dictionary.
        :type data: dict(str, object)
        """
        if use_handle:
            self._handle.seek(0)
            serialized = write_method(data, **self.kwargs)
            self._handle.write(serialized)
            self._handle.flush()
            os.fsync(self._handle.fileno())
            self._handle.truncate()
        else:
            write_method(self, data, **self.kwargs)
