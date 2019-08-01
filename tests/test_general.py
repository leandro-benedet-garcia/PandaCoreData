'''
:created: 18-07-2019

:author: Leandro (Cerberus1746) Benedet Garcia
'''
import pprint
import pytest
from panda_core_data import DataCore
from panda_core_data.custom_exceptions import (PCDFolderNotFound, PCDInvalidBaseData, PCDTypeError,
                                               PCDDataCoreIsNotUnique, PCDInvalidPathType)
from panda_core_data.data_core_bases.base_data import BaseData
from . import (MODEL_TYPE_NAME, MODEL_FILE, TEMPLATE_FILE)


class TestGeneral(object):
    @staticmethod
    def test_exceptions(tmpdir):
        data_core = DataCore(name="test_exceptions")
        with pytest.raises(PCDInvalidBaseData):
            #pylint: disable=unused-variable
            class DataTest(BaseData):
                pass

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
        data_core = DataCore(name="test_folders_exceptions")

        #===========================================================================================
        # file_structure["model_raw_dir"].join(f"{MODEL_TYPE_NAME}.yaml").write(YAML_CONTENT)
        # file_structure["raw_templates_dir"].join(f"{MODEL_TYPE_NAME}.yaml").write(YAML_CONTENT)
        #===========================================================================================

        file_structure["models_dir"].join(f"{MODEL_TYPE_NAME}.py").write(MODEL_FILE)
        file_structure["templates_dir"].join(f"{MODEL_TYPE_NAME}.py").write(TEMPLATE_FILE)

        mods_dir_path = str(file_structure["mods_dir"].realpath())
        with pytest.raises(PCDFolderNotFound):
            data_core("invalid")

        with pytest.raises(PCDFolderNotFound):
            data_core(mods_dir_path, core_mod_folder="invalid")

        with pytest.raises(PCDFolderNotFound):
            data_core(mods_dir_path, raws_folder="invalid")

        with pytest.raises(PCDFolderNotFound):
            data_core(mods_dir_path, models_folder="invalid")

        #===========================================================================================
        # with pytest.raises(PCDFolderIsEmpty):
        #     data_core(mods_dir_path)
        #===========================================================================================
