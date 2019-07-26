'''
:created: 09-07-2019

:author: Leandro (Cerberus1746) Benedet Garcia
'''

from dataclasses import fields, dataclass
import pytest

from panda_core_data import data_core
from panda_core_data.custom_exceptions import (PCDDuplicatedTypeName, PCDTypeGroupNotFound,
                                               PCDTypeNotFound)

from panda_core_data.model import Model
from panda_core_data.template import Template

from . import (DEFAULT_TEST_FIELD_CONTENT, DEFAULT_TEST_FIELD_NAME, INSTANCE_ERROR, MODEL_TYPE_NAME,
               MODEL_WITH_INIT_NAME, YAML_CONTENT)

class TestModels(object):
    @staticmethod
    def test_check_compatibility():
        class TemplateWithoutDataClass(Template):
            name: str

        class ModelWithoutDataClass(Model):
            name: str

        @dataclass
        class WithDataClass(object):
            name: str

        for template_data, model_data, with_data in zip(fields(TemplateWithoutDataClass),
                                                        fields(ModelWithoutDataClass),
                                                        fields(WithDataClass)):
            assert template_data.name == model_data.name == with_data.name
            assert template_data.type == model_data.type == with_data.type

    @staticmethod
    def test_repr(model, template):
        print(repr(model))
        print(repr(data_core.get_model_group()))

        print(repr(template))
        print(repr(data_core.get_template_group()))

    @staticmethod
    def test_default():
        assert data_core.get_model_type("invalid", default=False) is False
        assert data_core.get_template_type("invalid", default=False) is False

    @staticmethod
    def test_check_if_created(model, second_model, template, second_template):
        assert model in data_core.all_models
        assert second_model in data_core.all_models

        assert template in data_core.all_templates
        assert second_template in data_core.all_templates

    @staticmethod
    def test_check_if_unequal(model, second_model, model_with_init, template, second_template):
        assert template != second_template
        assert model != second_model != model_with_init

    @staticmethod
    def test_direct_instance_dataclass(model, template):
        model_type = data_core.get_model_type(MODEL_TYPE_NAME)
        instanced = model_type(DEFAULT_TEST_FIELD_CONTENT)

        assert isinstance(instanced, model), INSTANCE_ERROR
        assert getattr(instanced, DEFAULT_TEST_FIELD_NAME) == DEFAULT_TEST_FIELD_CONTENT

        instanced = model_type(name=DEFAULT_TEST_FIELD_CONTENT)
        assert instanced.name == DEFAULT_TEST_FIELD_CONTENT

        template_type = data_core.get_template_type(MODEL_TYPE_NAME)
        instanced = template_type(DEFAULT_TEST_FIELD_CONTENT)

        assert isinstance(instanced, template), INSTANCE_ERROR
        assert getattr(instanced, DEFAULT_TEST_FIELD_NAME) == DEFAULT_TEST_FIELD_CONTENT

        instanced = template_type(name=DEFAULT_TEST_FIELD_CONTENT)
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
    def test_exceptions(model, template):
        assert template
        with pytest.raises(PCDTypeGroupNotFound):
            #pylint: disable=unused-variable
            class TemplateGroupTesting(Template, group_name="invalid", auto_create_group=False):
                name: str

        with pytest.raises(PCDTypeNotFound):
            data_core.get_template_type("invalid")

        with pytest.raises(PCDDuplicatedTypeName):
            #pylint: disable=unused-variable
            class TestTemplate(Template, data_name=MODEL_TYPE_NAME):
                name: str

        with pytest.raises(PCDTypeGroupNotFound):
            #pylint: disable=unused-variable
            class ModelGroupTesting(Model, group_name="invalid", auto_create_group=False):
                name: str

        with pytest.raises(PCDTypeNotFound):
            data_core.get_model_type("invalid")

        with pytest.raises(FileNotFoundError):
            model(db_file="invalid")

        #pylint: disable=unused-variable
        with pytest.raises(PCDDuplicatedTypeName):  # @UndefinedVariable
            class TestModel(Model, data_name=MODEL_TYPE_NAME):
                name: str
