'''
:author: Leandro (Cerberus1746) Benedet Garcia
'''
from dataclasses import dataclass
from os.path import isdir
from .custom_exceptions import *

DEFAULT_MODEL_GROUP = "DEFAULT_MODEL_GROUP"
'''Default model group name, used for types and instances.'''

DEFAULT_TEMPLATE_GROUP = "DEFAULT_TEMPLATE_GROUP"
'''Default template group name, used for types and instances.'''

@dataclass
class Group(dict):
    group_name: str

class DataCore(object):
    """
    Class where everything is kept.
    """
    _all_model_groups = {}
    _all_template_groups = {}

    _all_models = {}
    _all_templates = {}

    raw_folders = []

    #def add_raw_folder(self, folder: str):
    #    """
    #    Add folder to the raws search path.
    #
    #    :param folder: folder to be added.
    #    :type folder: str
    #    """
    #    if not isdir(folder):
    #        raise FolderNotFound(f"The folder {folder} doesn't exist.")
    #    self.raw_folders.append(folder)

    @property
    def all_models(self):
        return list(self._all_models.values())

    @property
    def all_templates(self):
        return list(self._all_templates.values())

    @staticmethod
    def _wrapper_get_model_group(name: str, group_dict, default):
        group = group_dict.get(name, default)
        if not group and default is None:
            raise DataTypeGroupNotFound(f"Group '{name}' wasn't found.")

        return group

    @staticmethod
    def _wrapper_get_or_create_group(name: str, group_dict):
        return group_dict.setdefault(name, Group(name))

    def _wrapper_add_to_group(self, group_name: str, model, group_dict, data_type_dict,
                              auto_create_group):
        name = model.data_name

        if auto_create_group:
            group = self._wrapper_get_or_create_group(group_name, group_dict)
        else:
            group = self._wrapper_get_model_group(group_name, group_dict, None)

        if name not in data_type_dict:
            data_type_dict[name] = model

        if name in group:
            raise DuplicatedDataTypeName(f"There's already a {type(model)} with the name {name} "
                                         f"inside the group {group_name}.")

        model.data_group = group
        group[name] = model
        return group

    def _wrapper_get_model_type(self, name: str, group_dict, group_name: str, default,
                                group_default):
        group = self._wrapper_get_model_group(group_name, group_dict, default=group_default)
        if group:
            model = group.get(name, default)
            if not model and default is None:
                raise DataTypeNotFound(f"Model type {name} could not be found inside "
                                       f"the group {group_name}")
            return model
        return default

    def get_template_type(self, name: str, group_name: str = DEFAULT_MODEL_GROUP, default=None,
                          group_default=False):
        """
        Get model type from the group

        :param name: Name of the model type to get
        :type name: str
        :param group: Name of the group
        :type group: str
        :param default: Default value to be returned if model type is not found, if none, it will \
        raise an exception, which is the default.
        :type default: any
        :raises DataTypeNotFound: If the model doesn't exist.
        """
        return self._wrapper_get_model_type(name, self._all_template_groups, group_name, default,
                                            group_default)

    def add_template_to_group(self, group_name: str, model, auto_create_group=True):
        """
        Add a ~Template type to a group.

        If auto_create_group is true and the group doesn't exist it will be created.
        If false an exception will be raised.

        :param group_name: Name of the group
        :type group_name: str
        :param model: Model to be added
        :type model: Model
        :param auto_create_group: If the group should be created if it doesn't exist
        :type auto_create_group: bool
        :raises DuplicatedDataTypeName: If there's a model with the supplied name inside the group
        """
        self._wrapper_add_to_group(group_name, model, self._all_template_groups,
                                   self._all_templates, auto_create_group)


    def add_model_to_group(self, group_name: str, model, auto_create_group=True):
        """
        Add a ~Model type to a group.

        If auto_create_group is true and the group doesn't exist it will be created.
        If false an exception will be raised.

        :param group_name: Name of the group
        :type group_name: str
        :param model: Model to be added
        :type model: Model
        :param auto_create_group: If the group should be created if it doesn't exist
        :type auto_create_group: bool
        :raises DuplicatedDataTypeName: If there's a model with the supplied name inside the group
        """
        self._wrapper_add_to_group(group_name, model, self._all_model_groups, self._all_models,
                                   auto_create_group)

    def get_model_type(self, name: str, group_name: str = DEFAULT_MODEL_GROUP, default=None,
                       group_default=False):
        """
        Get model type from the group

        :param name: Name of the model type to get
        :type name: str
        :param group: Name of the group
        :type group: str
        :param default: Default value to be returned if model type is not found, if none, it will \
        raise an exception, which is the default.
        :type default: any
        :raises DataTypeNotFound: If the model doesn't exist.
        """
        return self._wrapper_get_model_type(name, self._all_model_groups, group_name, default,
                                            group_default)

    #def get_or_create_template_group(self, name: str):
    #    pass

#pylint: disable=invalid-name
data_core = DataCore()
