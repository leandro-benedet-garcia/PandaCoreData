'''
:author: Leandro (Cerberus1746) Benedet Garcia
'''
from os.path import isdir, join
from pathlib import Path
from typing import Optional

from .__version__ import __version__
from .custom_exceptions import (PCDDataCoreIsNotUnique, PCDInvalidPathType,
                                PCDTypeError, PCDInvalidPath)
from .custom_typings import PathType, Union
from .data_core_bases import BaseData
from .data_core_bases import DataModel
from .data_core_bases import DataTemplate
from .storages import auto_convert_to_pathlib


#pylint: disable=invalid-name
data_core = None


class DataCore(DataModel, DataTemplate):
    """Class where everything is kept."""

    def __init__(self, *args, name: Optional[str] = None,
                 replace: bool = False, **kwargs):
        """
        Start a new instance for the DataCore

        :param str name: name of the core data instance
        :param excluded_extensions: extensions to be ignored
        :param replace: if instances of data_core of the same name should
                             be replaced
        :type excluded_extensions: List[str]
        """
        self.folders = {}

        DataModel.__init__(self)
        DataTemplate.__init__(self)
        super().__init__(*args, **kwargs)

        self.name = name

        # pylint: disable=global-statement
        global data_core

        is_dict = isinstance(data_core, dict)
        has_name = name and is_dict
        if isinstance(data_core, DataCore) and name and name != "DEFAULT":
            old = data_core
            data_core = {}

            data_core["DEFAULT"] = old
            data_core[name] = self

        elif ((has_name and name not in data_core) or
              (replace and name and is_dict)):
            #pylint: disable=unsupported-assignment-operation
            data_core[name] = self

        elif has_name and name in data_core.keys():
            raise PCDDataCoreIsNotUnique(
                f"A data_core of the name {name} already exists")

        elif data_core is None:
            data_core = self

        else:
            raise PCDDataCoreIsNotUnique(
                "A DataCore instance already exists, you must set a name "
                "for any new instances now passing the parameter 'name' "
                "like this: 'DataCore(name='core_name')'. If you want to "
                "use the original instance, call it with "
                "data_core['DEFAULT']")

    def __call__(self, mods_path: PathType, core_mod_folder: PathType = "core",
                 raws_folder: PathType = "raws",
                 models_folder: PathType = "models",
                 templates_folder: PathType = "templates",
                 **kwargs: Union[str, bool]):
        """
        Automatically import all data types based on the paths in the params.

        :param mods_path: Absolute root folder to the root mods folder
        :param core_mod_folder: Name of the core mod folder. The base mod.
        :param raws_folder: Name of the raw folder.
        :param models_folder: Name of the models folder.
        :param templates_folder: Name of the templates folder.
        :param raw_models_folder: Name of the raws that are related to the
                                  models. Default is 'models_folder' param.
        :type raw_models_folder: :class:`~pathlib.Path` or str or bool
        :param raw_templates_folder: Name of the raws that are related to the
                                     templates. Default is the
                                     'templates_folder' param
        :type raw_templates_folder: :class:`~pathlib.Path` or str or bool
        :raise PCDInvalidPath: If any of the folders are invalid.
        """
        #=======================================================================
        # Extract params from kwarg
        #=======================================================================
        try:
            mods_path = auto_convert_to_pathlib(mods_path)
        except PCDInvalidPath as invalid_path:
            raise PCDInvalidPath(f"{invalid_path} This path must be absolute.")

        self.excluded_extensions = kwargs.pop(
            "excluded_extensions", self.excluded_extensions)

        raw_models_folder = kwargs.pop("raw_models_folder", models_folder)
        raw_templates_folder = kwargs.pop("raw_templates_folder",
                                          templates_folder)

        if any(kwargs):
            raise PCDTypeError(f"Invalid arguments supplied: {kwargs.keys()}")

        #=======================================================================
        # Check paths availability
        #=======================================================================

        core_folder = auto_convert_to_pathlib(join(mods_path, core_mod_folder))
        raws_folder = auto_convert_to_pathlib(join(core_folder, raws_folder))

        self.folders["models"] = join(core_folder, models_folder)
        self.folders["raw_models"] = join(raws_folder, raw_models_folder)

        if templates_folder:
            self.folders["templates"] = join(core_folder, templates_folder)
            self.folders["raw_templates"] = join(
                raws_folder, raw_templates_folder)

        for param_name, path in self.folders.items():
            try:
                path = auto_convert_to_pathlib(path)
                self.folders[param_name] = path
            except PCDInvalidPath as invalid_path:
                raise PCDInvalidPath(
                    f"{invalid_path} It must be relative from the core mod "
                    f"path which is set to {core_folder}' or the 'raw_folder' "
                    f"that is '{raws_folder}'.")

        # Import models and templates
        self.recursively_add_module(self.get_folder("models"))

        if templates_folder:
            self.recursively_add_module(self.get_folder("templates"))
            self.recursively_instance_template(self.get_folder("raw_templates"))

        self.recursively_instance_model(self.get_folder("raw_models"))

        for current_instance in self.all_model_instances:
            if current_instance.has_dependencies:
                current_instance.add_dependencies()

    def get_folder(self, folder_type):
        try:
            return self.folders[folder_type]
        except KeyError:
            raise PCDInvalidPathType(
                f"The folder type {folder_type} could not be found. The "
                f"valid folder types are {list(self.folders.keys())}")


DataCore()
