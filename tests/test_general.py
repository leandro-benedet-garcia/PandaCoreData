'''
:created: 18-07-2019

:author: Leandro (Cerberus1746) Benedet Garcia
'''
import pprint
import pytest

from panda_core_data import DataCore
from panda_core_data.custom_exceptions import (PCDInvalidPath, PCDInvalidBaseData, PCDTypeError,
                                               PCDDataCoreIsNotUnique, PCDInvalidPathType,
                                               PCDDuplicatedModuleName, PCDRawFileNotSupported,
                                               PCDFolderIsEmpty)
from panda_core_data.data_core_bases.base_data import BaseData

from panda_core_data.storages import (get_extension, get_storage_from_extension,
                                      is_excluded_extension)

from . import (MODEL_TYPE_NAME, MODEL_FILE, TEMPLATE_FILE)


class TestGeneral(object):
    @staticmethod
    def test_storage_utils(tmpdir):
        test_json = tmpdir.join("test.json")
        test_json.write("")

        assert get_extension(test_json.realpath()) == "json"
        assert is_excluded_extension("json", ["json",]) is True

        with pytest.raises(PCDRawFileNotSupported):
            get_storage_from_extension("py")

    @staticmethod
    def test_exceptions(tmpdir):
        core_name = "general_test_exceptions"
        data_core = DataCore(name=core_name)

        with pytest.raises(PCDInvalidBaseData):
            #pylint: disable=unused-variable
            class DataTest(BaseData):
                pass

        with pytest.raises(PCDDataCoreIsNotUnique):
            DataCore(name=core_name)

        with pytest.raises(PCDTypeError):
            mods_dir = tmpdir.mkdir("mods")
            data_core(mods_dir.realpath(), invalid="invalid")

        with pytest.raises(PCDDataCoreIsNotUnique):
            DataCore()
            DataCore()

        with pytest.raises(PCDInvalidPathType):
            data_core.get_folder("invalid")

    @staticmethod
    def test_folders_exceptions(file_structure):
        pwetty = pprint.PrettyPrinter()
        pwetty.pprint(file_structure)
        core_name = "test_folders_exceptions"

        data_core = DataCore(name=core_name)

        with pytest.raises(PCDFolderIsEmpty):
            data_core.recursively_instance_model(file_structure["models_dir"].realpath())

        with pytest.raises(PCDFolderIsEmpty):
            data_core.folder_contents(file_structure["models_dir"])

        model_content = MODEL_FILE.replace("CORE_NAME", core_name)
        template_content = TEMPLATE_FILE.replace("CORE_NAME", core_name)

        file_structure["models_dir"].join(f"{MODEL_TYPE_NAME}.py").write(model_content)
        file_structure["templates_dir"].join(f"{MODEL_TYPE_NAME}.py").write(template_content)

        mods_dir_path = str(file_structure["mods_dir"].realpath())
        with pytest.raises(PCDInvalidPath):
            data_core("invalid")

        with pytest.raises(PCDDuplicatedModuleName):
            file_structure["models_dir"].join(f"test.py").write(model_content)
            file_structure["templates_dir"].join(f"test.py").write(template_content)
            data_core(mods_dir_path)

        with pytest.raises(PCDInvalidPath):
            data_core(mods_dir_path, core_mod_folder="invalid")

        with pytest.raises(PCDInvalidPath):
            data_core(mods_dir_path, raws_folder="invalid")

        with pytest.raises(PCDInvalidPath):
            data_core(mods_dir_path, models_folder="invalid")

        with pytest.raises(PCDInvalidPathType):
            file_structure["models_dir"].join("file.json").write("")
            data_core.recursively_instance_model(file_structure["models_dir"])

    @staticmethod
    def test_exclusions(file_structure):
        pwetty = pprint.PrettyPrinter()
        pwetty.pprint(file_structure)

        core_name = "test_exclusions"
        data_core = DataCore(name=core_name)

        model_content = MODEL_FILE.replace("CORE_NAME", core_name)
        template_content = TEMPLATE_FILE.replace("CORE_NAME", core_name)

        file_structure["models_dir"].join(f"meta.meta").write("")
        file_structure["root_model_raw_dir"].join(f"meta.meta").write("")
        file_structure["templates_dir"].join(f"meta.meta").write("")

        file_structure["models_dir"].join(f"ext{MODEL_TYPE_NAME}.py").write(model_content)
        file_structure["templates_dir"].join(f"exts{MODEL_TYPE_NAME}.py").write(template_content)

        mods_dir_path = str(file_structure["mods_dir"].realpath())
        data_core(mods_dir_path, excluded_extensions=["meta",])
