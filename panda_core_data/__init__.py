'''
:author: Leandro (Cerberus1746) Benedet Garcia
'''
from os.path import isdir, join

from .data_core_bases import DataModel
from .data_core_bases import DataTemplate
from .data_core_bases import BaseData
from .__version__ import __version__
from .utils import auto_convert_to_pathlib

from .custom_exceptions import (PCDDataCoreIsNotUnique, PCDInvalidPathType, PCDTypeError,
                                PCDFolderNotFound)

#pylint: disable=invalid-name
data_core = None

class DataCore(DataModel, DataTemplate):
    """
    Class where everything is kept.
    """

    def __init__(self, name=None):
        self.folders = {}

        DataModel.__init__(self)
        DataTemplate.__init__(self)

        #pylint: disable=global-statement
        global data_core
        if isinstance(data_core, DataCore) and name:
            old = data_core
            data_core = {}

            data_core["DEFAULT"] = old
            data_core[name] = self

        elif name and isinstance(data_core, dict):
            #pylint: disable=unsupported-assignment-operation
            data_core[name] = self

        elif data_core is None:
            data_core = self

        else:
            raise PCDDataCoreIsNotUnique("A DataCore instance already exists, you must set a name "
                                         "for any new instances now. And to use the original "
                                         "use data_core['DEFAULT']")


    def __call__(self, mods_path, **kwargs):
        """
        Automatically import all data types based on the paths in the params.

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
        #===========================================================================================
        # Extract params from kwarg
        #===========================================================================================
        try:
            mods_path = auto_convert_to_pathlib(mods_path, True)
        except PCDFolderNotFound as invalid_path:
            raise PCDFolderNotFound(f"{invalid_path} This path must be absolute.")

        core_mod_folder = kwargs.pop("core_mod_folder", "core")
        raws_folder = kwargs.pop("raws_folder", "raws")
        models_folder = kwargs.pop("models_folder", "models")
        templates_folder = kwargs.pop("templates_folder", "templates")

        raw_models_folder = kwargs.pop("raw_models_folder", models_folder)
        raw_templates_folder = kwargs.pop("raw_templates_folder", templates_folder)

        if any(kwargs):
            raise PCDTypeError(f"Invalid arguments supplied: {kwargs.keys()}")

        #===========================================================================================
        # Check paths availability
        #===========================================================================================

        core_folder = auto_convert_to_pathlib(join(mods_path, core_mod_folder), True)
        raws_folder = auto_convert_to_pathlib(join(core_folder, raws_folder), True)

        self.folders["models"] = join(core_folder, models_folder)
        self.folders["raw_models"] = join(raws_folder, raw_models_folder)

        if templates_folder:
            self.folders["templates"] = join(core_folder, templates_folder)
            self.folders["raw_templates"] = join(raws_folder, raw_templates_folder)

        for param_name, path in self.folders.items():
            try:
                path = auto_convert_to_pathlib(path, True)
                self.folders[param_name] = path
            except PCDFolderNotFound as invalid_path:
                raise PCDFolderNotFound(f"{invalid_path} It must be relative from the core mod "
                                        f"path which is set to {core_folder}' or the 'raw_folder' "
                                        f"that is '{raws_folder}'.")

        # Import models and templates
        self.recursively_add_model_module(self.get_folder("models"))

        if templates_folder:
            self.recursively_add_template_module(self.get_folder("templates"))
            self.recursively_instance_template(self.get_folder("raw_templates"))

        self.recursively_instance_model(self.get_folder("raw_models"))

        for current_instance in self.all_model_instances:
            if current_instance.has_dependencies:
                current_instance.add_dependencies()

    def get_folder(self, folder_type):
        try:
            return self.folders[folder_type]
        except KeyError:
            raise PCDInvalidPathType(f"The folder type {folder_type} could not be found. The "
                                     f"valid folder types are {list(self.folders.keys())}")

__all__ = ["data_core", "DataCore", "DataModel", "DataTemplate", "BaseData"]
DataCore()
