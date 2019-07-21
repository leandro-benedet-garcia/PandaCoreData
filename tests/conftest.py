import pytest

from panda_core_data.model import Model
from panda_core_data.template import Template
#pylint: disable=unused-import
from . import (MODEL_TYPE_NAME, MODEL_WITH_INIT_NAME, DEFAULT_TEST_FIELD_CONTENT,
               SECOND_MODEL_TYPE_NAME)

#pylint: disable=invalid-name
type_name = ""
def create_test_model(model_name):
    #pylint: disable=redefined-outer-name
    #pylint: disable=unused-variable
    type_name = model_name
    class TestModel(Model, data_name=type_name, replace=True):
        name: str

    return TestModel

@pytest.fixture
def model():
    return create_test_model(MODEL_TYPE_NAME)

@pytest.fixture
def model_with_init():
    class TestModelWithInit(Model, data_name=MODEL_WITH_INIT_NAME, replace=True):
        name: str

        #pylint: disable=super-init-not-called
        def __init__(self):
            self.name = DEFAULT_TEST_FIELD_CONTENT


    return TestModelWithInit

@pytest.fixture
def second_model():
    return create_test_model(SECOND_MODEL_TYPE_NAME)

def create_test_template(template_name):
    #pylint: disable=redefined-outer-name
    #pylint: disable=unused-variable
    type_name = template_name
    class TestTemplate(Template, data_name=type_name, replace=True):
        name: str

    return TestTemplate

@pytest.fixture
def template():
    return create_test_template(MODEL_TYPE_NAME)

@pytest.fixture
def second_template():
    return create_test_template(SECOND_MODEL_TYPE_NAME)
