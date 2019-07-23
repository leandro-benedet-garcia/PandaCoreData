'''
:created: 2019-07-22

:author: Leandro (Cerberus1746) Benedet Garcia
'''
from os.path import isdir, join

from .data_core_bases.data_model import DataModel
from .data_core_bases.data_template import DataTemplate

from .custom_exceptions import PCDDataCoreIsNotUnique, PCDFolderNotFound, PCDInvalidFolderType

class DataCore(DataModel, DataTemplate):
    """
    Class where everything is kept.
    """
    _instance = None

    folders: dict

    def __new__(cls):
        if DataCore._instance is None:
            DataCore._instance = object.__new__(cls)
            return DataCore._instance

        raise PCDDataCoreIsNotUnique("Data core instance must be unique.")

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
            self._check_if_path_exists(mods_path, "mods_path")
        except PCDFolderNotFound as invalid_path:
            raise PCDFolderNotFound(f"{invalid_path} This path must be absolute.")

        core_mod_folder = kwargs.pop("core_mod_folder", "core")
        raws_folder = kwargs.pop("raws_folder", "raws")
        models_folder = kwargs.pop("models_folder", "models")
        templates_folder = kwargs.pop("templates_folder", "templates")

        raw_models_folder = kwargs.pop("raw_models_folder", models_folder)
        raw_templates_folder = kwargs.pop("raw_templates_folder", templates_folder)

        #===========================================================================================
        # Check paths availability
        #===========================================================================================

        core_folder = join(mods_path, core_mod_folder)
        self._check_if_path_exists(core_folder, "core_mod_folder")

        raws_folder = join(core_folder, raws_folder)
        self._check_if_path_exists(raws_folder, "raws_folder")

        self.folders = {
            "models": join(core_folder, models_folder),
            "templates": join(core_folder, templates_folder),

            "raw_models": join(raws_folder, raw_models_folder),
            "raw_templates": join(raws_folder, raw_templates_folder),
        }

        for param_name, path in self.folders.items():
            param_name += "_folder"
            if not locals().get(param_name):
                continue
            try:
                self._check_if_path_exists(path, param_name)
            except PCDFolderNotFound as invalid_path:
                raise PCDFolderNotFound(f"{invalid_path} It must be relative from the core mod "
                                        f"path which is set to {core_folder}' or the 'raw_folder' "
                                        f"that is '{raws_folder}'.")

        # Import models and templates
        self.add_model_module(self.get_folder("models"))
        self.add_template_module(self.get_folder("templates"))

        self.recursively_instance_template(self.get_folder("raw_templates"))
        #self.recursively_instance_model(self.get_folder("raw_models"))

        #===========================================================================================
        # for model_type in self.all_models:
        #     if model_type.has_dependencies:
        #         model_type.add_dependencies(model_type)
        #===========================================================================================

    def get_folder(self, folder_type):
        try:
            return self.folders[folder_type]
        except KeyError:
            raise PCDInvalidFolderType(f"The folder type {folder_type} could not be found. The "
                                       f"valid folder types are {list(self.folders.keys())}")

    @staticmethod
    def _check_if_path_exists(path, param_name):
        if not isdir(path):
            raise PCDFolderNotFound(f"The folder {path} doesn't exist. Make sure you set "
                                    f"your '{param_name}' parameter correctly")
