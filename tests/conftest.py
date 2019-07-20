import pytest
from panda_core_data import data_core
from panda_core_data.model import Model
from panda_core_data.template import Template
from . import (MODEL_TYPE_NAME, MODEL_WITH_INIT_NAME, DEFAULT_TEST_FIELD_CONTENT,
               SECOND_MODEL_TYPE_NAME)

def create_test_model(model_name):
    test_model = data_core.get_model_type(model_name, default=False, group_default=False)
    if not test_model:
        class TestModel(Model, model_name=model_name):
            name: str

        test_model = TestModel

    return test_model

@pytest.fixture
def model():
    return create_test_model(MODEL_TYPE_NAME)

@pytest.fixture
def model_with_init():
    test_model = data_core.get_model_type(MODEL_WITH_INIT_NAME, default=False)
    if not test_model:
        class TestModelWithInit(Model, model_name=MODEL_WITH_INIT_NAME):
            name: str

            #pylint: disable=super-init-not-called
            def __init__(self):
                self.name = DEFAULT_TEST_FIELD_CONTENT

        test_model = TestModelWithInit

    return test_model

@pytest.fixture
def second_model():
    return create_test_model(SECOND_MODEL_TYPE_NAME)

def create_test_template(template_name):
    test_template = data_core.get_template_type(template_name, default=False, group_default=False)
    if not test_template:
        class TestModel(Template, template_name=template_name):
            name: str

        test_template = TestModel

    return test_template

@pytest.fixture
def template():
    return create_test_template(MODEL_TYPE_NAME)

@pytest.fixture
def second_template():
    return create_test_template(SECOND_MODEL_TYPE_NAME)
