'''
:created: 18-07-2019

:author: Leandro (Cerberus1746) Benedet Garcia
'''
import pytest
from panda_core_data import DataCore, data_core
from panda_core_data.custom_exceptions import (PCDDataCoreIsNotUnique, PCDFolderNotFound,
                                               PCDInvalidBaseData)
from panda_core_data.data_core_bases.base_data import BaseData

from . import YAML_CONTENT, MODEL_TYPE_NAME, MODEL_FILE, TEMPLATE_FILE


class TestGeneral(object):
    @staticmethod
    def test_default():
        assert data_core.get_model_type("invalid", default=False) is False
        assert data_core.get_template_type("invalid", default=False) is False

    @staticmethod
    def test_repr(model):
        print(repr(model))
        print(repr(data_core.get_model_group()))
        assert repr(model) in repr(data_core.get_model_group())

    @staticmethod
    def test_bases():
        with pytest.raises(PCDInvalidBaseData):
            #pylint: disable=unused-variable
            class DataTest(BaseData):
                pass

    @staticmethod
    def test_folders_exceptions(tmpdir):
        mods_dir = tmpdir.mkdir("mods")
        core_dir = mods_dir.mkdir("core")

        models_dir = core_dir.mkdir("models")
        templates_dir = core_dir.mkdir("templates")

        raws_dir = core_dir.mkdir("raws")
        raw_models_dir = raws_dir.mkdir("models")
        raw_templates_dir = raws_dir.mkdir("templates")

        raw_models_dir.join(f"{MODEL_TYPE_NAME}.yaml").write(YAML_CONTENT)
        raw_templates_dir.join(f"{MODEL_TYPE_NAME}.yaml").write(YAML_CONTENT)

        models_dir.join(f"{MODEL_TYPE_NAME}.py").write(MODEL_FILE)
        templates_dir.join(f"{MODEL_TYPE_NAME}.py").write(TEMPLATE_FILE)

        mods_dir_path = str(mods_dir.realpath())
        with pytest.raises(PCDDataCoreIsNotUnique):
            DataCore()

        with pytest.raises(PCDFolderNotFound):
            data_core("invalid")

        with pytest.raises(PCDFolderNotFound):
            data_core(mods_dir_path, core_mod_folder="invalid")

        with pytest.raises(PCDFolderNotFound):
            data_core(mods_dir_path, raws_folder="invalid")

        with pytest.raises(PCDFolderNotFound):
            data_core(mods_dir_path, models_folder="invalid")
