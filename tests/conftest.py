import pytest

from panda_core_data.model import Model, Template
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

@pytest.fixture
def file_structure(tmpdir):
    return_dict = {}
    mods_dir = tmpdir.mkdir("mods")
    core_dir = mods_dir.mkdir("core")
    raws_dir = core_dir.mkdir("raws")

    return_dict["mods_dir"] = mods_dir
    return_dict["raws_dir"] = raws_dir
    return_dict["core_dir"] = core_dir

    return_dict["models_dir"] = core_dir.mkdir("models")
    return_dict["templates_dir"] = core_dir.mkdir("templates")

    return_dict["root_model_raw_dir"] = raws_dir.mkdir("models")
    return_dict["model_raw_dir"] = return_dict["root_model_raw_dir"].mkdir(MODEL_TYPE_NAME)
    return_dict["raw_templates_dir"] = return_dict["raws_dir"].mkdir("templates")

    return return_dict
