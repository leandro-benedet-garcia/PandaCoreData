'''
:created: 09-07-2019

:author: Leandro (Cerberus1746) Benedet Garcia
'''
import pytest

from panda_core_data import data_core
from panda_core_data.custom_exceptions import DuplicatedDataTypeName, DataTypeGroupNotFound,\
    DataTypeNotFound
from panda_core_data.model import Model

from . import (DEFAULT_TEST_FIELD_CONTENT, DEFAULT_TEST_FIELD_NAME, INSTANCE_ERROR, MODEL_TYPE_NAME,
               MODEL_WITH_INIT_NAME, SECOND_MODEL_TYPE_NAME, YAML_CONTENT)

class TestModels(object):
    @staticmethod
    def create_test_model(model_name):
        test_model = data_core.get_model_type(model_name, default=False)
        if not test_model:
            class TestModel(Model, model_name=model_name):
                name: str

            test_model = TestModel

        return test_model

    @pytest.fixture
    def model(self):
        return self.create_test_model(MODEL_TYPE_NAME)

    @pytest.fixture
    def model_with_init(self):
        test_model = data_core.get_model_type(
            MODEL_WITH_INIT_NAME, default=False)
        if not test_model:
            class TestModelWithInit(Model, model_name=MODEL_WITH_INIT_NAME):
                name: str

                #pylint: disable=super-init-not-called
                def __init__(self):
                    self.name = DEFAULT_TEST_FIELD_CONTENT

            test_model = TestModelWithInit

        return test_model

    @pytest.fixture
    def second_model(self):
        return self.create_test_model(SECOND_MODEL_TYPE_NAME)

    @staticmethod
    def test_check_if_equal(model):
        assert data_core.get_model_type(MODEL_TYPE_NAME) == model

    @staticmethod
    def test_check_if_unequal(model, second_model, model_with_init):
        assert model != second_model != model_with_init

    @staticmethod
    def test_direct_instance_dataclass(model):
        model_type = data_core.get_model_type(MODEL_TYPE_NAME)
        instanced = model_type(DEFAULT_TEST_FIELD_CONTENT)

        assert isinstance(instanced, model), INSTANCE_ERROR
        assert getattr(
            instanced, DEFAULT_TEST_FIELD_NAME) == DEFAULT_TEST_FIELD_CONTENT

        instanced = model_type(name=DEFAULT_TEST_FIELD_CONTENT)
        assert instanced.name == DEFAULT_TEST_FIELD_CONTENT

    @staticmethod
    def test_dataclass_with_init(model_with_init):
        model_type = data_core.get_model_type(MODEL_WITH_INIT_NAME)
        instanced = model_type()

        assert isinstance(instanced, model_with_init), INSTANCE_ERROR
        assert getattr(
            instanced, DEFAULT_TEST_FIELD_NAME) == DEFAULT_TEST_FIELD_CONTENT

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
        #pylint: disable=unused-variable
        with pytest.raises(DataTypeGroupNotFound):  # @UndefinedVariable
            #pylint: disable=unused-variable
            class GroupTesting(Model, model_group_name="invalid", auto_create_group=False):
                name: str

        #pylint: disable=unused-variable
        with pytest.raises(DataTypeNotFound):  # @UndefinedVariable
            data_core.get_model_type("invalid")

        #pylint: disable=unused-variable
        with pytest.raises(FileNotFoundError):  # @UndefinedVariable
            model(db_file="invalid")

        #pylint: disable=unused-variable
        with pytest.raises(DuplicatedDataTypeName):  # @UndefinedVariable
            class TestModel(Model, model_name=MODEL_TYPE_NAME):
                name: str
