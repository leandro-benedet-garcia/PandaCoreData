'''
:created: 09-07-2019

:author: Leandro (Cerberus1746) Benedet Garcia
'''
import pytest

from panda_core_data import data_core
from panda_core_data.custom_exceptions import PCDDuplicatedTypeName, PCDTypeGroupNotFound,\
    PCDTypeNotFound
from panda_core_data.model import Model

from . import (DEFAULT_TEST_FIELD_CONTENT, DEFAULT_TEST_FIELD_NAME, INSTANCE_ERROR, MODEL_TYPE_NAME,
               MODEL_WITH_INIT_NAME, YAML_CONTENT)

class TestModels(object):
    @staticmethod
    def test_check_if_created(model, second_model):
        assert model in data_core.all_models
        assert second_model in data_core.all_models

    @staticmethod
    def test_check_if_unequal(model, second_model, model_with_init):
        assert model != second_model != model_with_init

    @staticmethod
    def test_direct_instance_dataclass(model):
        model_type = data_core.get_model_type(MODEL_TYPE_NAME)
        instanced = model_type(DEFAULT_TEST_FIELD_CONTENT)

        assert isinstance(instanced, model), INSTANCE_ERROR
        assert getattr(instanced, DEFAULT_TEST_FIELD_NAME) == DEFAULT_TEST_FIELD_CONTENT

        instanced = model_type(name=DEFAULT_TEST_FIELD_CONTENT)
        assert instanced.name == DEFAULT_TEST_FIELD_CONTENT

    @staticmethod
    def test_dataclass_with_init(model_with_init):
        model_type = data_core.get_model_type(MODEL_WITH_INIT_NAME)
        instanced = model_type()

        assert isinstance(instanced, model_with_init), INSTANCE_ERROR
        assert getattr(instanced, DEFAULT_TEST_FIELD_NAME) == DEFAULT_TEST_FIELD_CONTENT

    @staticmethod
    def test_load_from_file(tmpdir, model):
        tmp_dir = tmpdir.mkdir("raws")
        yaml_file = tmp_dir.join("test.yaml")
        yaml_file_path = str(yaml_file.realpath())

        yaml_file.write(YAML_CONTENT)

        instanced = model(db_file=yaml_file_path)
        assert isinstance(instanced, model), INSTANCE_ERROR
        assert getattr(instanced, DEFAULT_TEST_FIELD_NAME) == DEFAULT_TEST_FIELD_CONTENT


    def test_post_init_with_file(self, tmpdir):
        #pylint: disable=unused-variable
        class TestModelWithPostInit(Model):
            name: str

            def __post_init__(self):
                default_field = DEFAULT_TEST_FIELD_NAME
                assert getattr(self, default_field) == DEFAULT_TEST_FIELD_CONTENT
                self.name = "another_content"

        model_class = data_core.get_model_type("TestModelWithPostInit")
        tmp_dir = tmpdir.mkdir("raws")
        yaml_file = tmp_dir.join("test.yaml")
        yaml_file_path = str(yaml_file.realpath())

        yaml_file.write(YAML_CONTENT)

        instanced = model_class(db_file=yaml_file_path)
        assert isinstance(instanced, model_class), INSTANCE_ERROR
        assert getattr(instanced, DEFAULT_TEST_FIELD_NAME) == "another_content"

    @staticmethod
    def test_exceptions(model):
        with pytest.raises(PCDTypeGroupNotFound):
            #pylint: disable=unused-variable
            class GroupTesting(Model, group_name="invalid", auto_create_group=False):
                name: str

        with pytest.raises(PCDTypeNotFound):
            data_core.get_model_type("invalid")

        with pytest.raises(FileNotFoundError):
            model(db_file="invalid")

        #pylint: disable=unused-variable
        with pytest.raises(PCDDuplicatedTypeName):  # @UndefinedVariable
            class TestModel(Model, data_name=MODEL_TYPE_NAME):
                name: str
