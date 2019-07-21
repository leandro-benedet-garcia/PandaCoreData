'''
:author: Leandro (Cerberus1746) Benedet Garcia
'''
from dataclasses import dataclass

from os import walk
from os.path import isdir, join
from glob import iglob

import sys
from pathlib import Path
from importlib import import_module

from .custom_exceptions import *

DEFAULT_MODEL_GROUP = "DEFAULT_MODEL_GROUP"
'''Default model group name, used for types and instances.'''

DEFAULT_TEMPLATE_GROUP = "DEFAULT_TEMPLATE_GROUP"
'''Default template group name, used for types and instances.'''

@dataclass
class Group(dict):
    """
    Class that is used to store Models or Templates
    """
    group_name: str

class DataCore(object):
    """
    Class where everything is kept.
    """
    _instance = None

    all_model_groups = Group("all_model_groups")
    all_template_groups = Group("all_template_groups")

    all_key_value_models = Group("all_models")
    all_key_value_templates = Group("all_templates")

    model_modules = []
    template_modules = []

    raw_models = []
    raw_templates = []

    raw_model_folders = []
    raw_template_folders = []

    def __new__(cls):
        if DataCore._instance is None:
            DataCore._instance = object.__new__(cls)
            return DataCore._instance

        raise PCDDataCoreIsNotUnique("Data core instance must be unique.")

    def __call__(self, mods_path, **kwargs):
        """
        Automatically import all templates based on the paths in the params.

        :param mods_path: Absolute root folder to the root mods folder
        :type mods_path: str
        :param core_mod_folder: Name of the core mod folder. The base mod.
        :type core_mod_folder: str
        :param raws_folder: Name of the raw folder.
        :type raws_folder: str
        :param models_folder: Name of the models folder.
        :type models_folder: str
        :param templates_folder: Name of the templates folder.
        :type templates_folder: str
        :param raw_models_folder: Name of the raws that are related to the models. Default is \
        'models_folder' param.
        :type raw_models_folder: str
        :param raw_templates_folder: Name of the raws that are related to the templates. Default \
        is the 'templates_folder' param
        :type raw_templates_folder: str
        :raise PCDFolderNotFound: If any of the folders are invalid.
        """
        if not isdir(mods_path):
            raise PCDFolderNotFound(f"The folder '{mods_path}' doesn't exist. It must be absolute.")

        core_mod_folder = kwargs.pop("core_mod_folder", "core")
        raws_folder = kwargs.pop("raws_folder", "raws")
        models_folder = kwargs.pop("models_folder", "models")
        templates_folder = kwargs.pop("templates_folder", "templates")

        raw_models_folder = kwargs.pop("raw_models_folder", models_folder)
        raw_templates_folder = kwargs.pop("raw_templates_folder", templates_folder)

        core_folder = join(mods_path, core_mod_folder)
        if not isdir(core_folder):
            raise PCDFolderNotFound(f"The folder {core_folder} doesn't exist. Make sure you set "
                                    "your 'core_mod_folder' parameter correctly")

        raws_folder = join(core_folder, raws_folder)
        if not isdir(raws_folder):
            raise PCDFolderNotFound(f"The folder {raws_folder} doesn't exist. Make sure you set "
                                    "your 'raws_folder' parameter correctly, it must be relative "
                                    f"from your 'core_mod_folder' which is '{core_mod_folder}'.")

        # Just setting the key names as the parameters so they can be shown in the exception inside
        # the for loop.
        folders = {
            "models_folder": join(core_folder, models_folder),
            "templates_folder": join(core_folder, templates_folder),

            "raw_models_folder": join(raws_folder, raw_models_folder),
            "raw_templates_folder": join(raws_folder, raw_templates_folder),
        }

        for param_name, path in folders.items():
            if not isdir(path) and locals().get(param_name):
                raise PCDFolderNotFound(f"The folder '{path}' doesn't exist. Make sure you set "
                                        f"your '{param_name}' parameter correctly. It must be "
                                        "relative from the core mod path which is set to "
                                        f"'{core_folder}' or the 'raw_folder' that "
                                        f"is '{raws_folder}'.")

            # Dynamically import models and templates
            if param_name in ["models_folder", "templates_folder"]:
                sys.path.append(path)

                for py_file in iglob(join(path, '*.py')):
                    module_name = Path(py_file).stem
                    getattr(self, param_name.replace("s_folder", "_modules")).append(
                        import_module(module_name)
                    )

            elif param_name in ["raw_models_folder", "raw_templates_folder"]:
                getattr(self, param_name.replace("s_folder", "_folders")).append(path)

                for raw_file in iglob(join(path, '*.yaml')):
                    raw = Path(raw_file).stem
                    if param_name == "raw_models_folder":
                        print(self.get_model_type(raw)(db_file=raw_file))
                    #===============================================================================
                    # elif param_name == "raw_templates_folder":
                    #     print(self.get_template_type(raw)(db_file=raw_file))
                    #===============================================================================


        #===========================================================================================
        # for model_type in self.all_models:
        #     if model_type.has_dependencies:
        #         model_type.add_dependencies(model_type)
        #===========================================================================================

    @staticmethod
    def _wrapper_get_group(name: str, group_dict, default):
        group = group_dict.get(name, default)
        if not group and default is None:
            raise PCDTypeGroupNotFound(f"Group '{name}' wasn't found.")

        return group

    @staticmethod
    def _wrapper_get_or_create_group(name: str, group_dict):
        return group_dict.setdefault(name, Group(name))

    def _wrapper_get_model_type(self, name: str, group_dict, group_name: str, default,
                                group_default):
        group = self._wrapper_get_group(group_name, group_dict, default=group_default)
        if group:
            model = group.get(name, default)
            if not model and default is None:
                raise PCDTypeNotFound(f"Model type {name} could not be found inside "
                                      f"the group {group_name}")
            return model
        return default

    @property
    def all_models(self):
        return list(self.all_key_value_models.values())

    @property
    def all_templates(self):
        return list(self.all_key_value_templates.values())

    def wrapper_add_to_group(self, group_name: str, model, group_dict, auto_create_group, replace):
        name = model.data_name
        if auto_create_group:
            group = self._wrapper_get_or_create_group(group_name, group_dict)
        else:
            group = self._wrapper_get_group(group_name, group_dict, None)

        if not replace and name in group:
            raise PCDDuplicatedTypeName(f"There's already a {type(model)} with the name {name} "
                                        f"inside the group {group_name}.")

        model.data_group = group
        group[name] = model
        return group

    def get_template_type(self, name: str, group_name: str = DEFAULT_MODEL_GROUP, default=None,
                          group_default=None):
        """
        Get :class:`panda_core_data.template.Template` type from the group

        :param name: Name of the :class:`panda_core_data.template.Template` type to get
        :type name: str
        :param group: Name of the group
        :type group: str
        :param default: Default value to be returned if model type is not found, if none, it will \
        raise an exception, which is the default.
        :type default: any
        :returns: The :class:`panda_core_data.template.Template` type
        :raises PCDTypeNotFound: If the model doesn't exist.
        """
        return self._wrapper_get_model_type(name, self.all_template_groups, group_name, default,
                                            group_default)

    def add_template_to_group(self, group_name: str, model, auto_create_group: bool = True):
        """
        Add a :class:`panda_core_data.template.Template` type to a group.

        If auto_create_group is true and the group doesn't exist it will be created.
        If false an exception will be raised.

        :param group_name: Name of the group
        :type group_name: str
        :param model: :class:`Template` to be added
        :type model: Template
        :param auto_create_group: If the group should be created if it doesn't exist
        :type auto_create_group: bool
        :raises PCDDuplicatedTypeName: If there's a model with the supplied name inside the group
        """
        self.wrapper_add_to_group(group_name, model, self.all_template_groups, auto_create_group,
                                  False)


    def add_model_to_group(self, group_name: str, model, auto_create_group=True):
        """
        Add a :class:`panda_core_data.template.Model` type to a group.

        If auto_create_group is true and the group doesn't exist it will be created.
        If false an exception will be raised.

        :param group_name: Name of the group
        :type group_name: str
        :param model: :class:`panda_core_data.template.Model` to be added
        :type model: Model
        :param auto_create_group: If the group should be created if it doesn't exist
        :type auto_create_group: bool
        :raises PCDDuplicatedTypeName: If there's a model with the supplied name inside the group
        """
        self.wrapper_add_to_group(group_name, model, self.all_model_groups,
                                  auto_create_group, False)

    def get_model_type(self, name: str, group_name: str = DEFAULT_MODEL_GROUP, default=None,
                       group_default=None):
        """
        Get :class:`panda_core_data.template.Model` type from the group

        :param name: Name of the model type to get
        :type name: str
        :param group: Name of the group
        :type group: str
        :param default: Default value to be returned if model type is not found, if none, it will \
        raise an exception, which is the default.
        :type default: any
        :returns: The :class:`panda_core_data.template.Model` type.
        :raises PCDTypeNotFound: If the model doesn't exist.
        """
        return self._wrapper_get_model_type(name, self.all_model_groups, group_name, default,
                                            group_default)


#pylint: disable=invalid-name
data_core = DataCore()
