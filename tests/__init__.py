MODEL_TYPE_NAME = "model_type_name"
SECOND_MODEL_TYPE_NAME = "second_model_type_name"
MODEL_WITH_INIT_NAME = "model_with_init_name"
CREATION_TEST_NAME = "creation_test_name"

DEFAULT_TEST_FIELD_NAME = "name"
DEFAULT_TEST_FIELD_CONTENT = "name_content"

YAML_CONTENT = f"""
data:
    - {DEFAULT_TEST_FIELD_NAME}: {DEFAULT_TEST_FIELD_CONTENT}
""".strip()

MODEL_FILE = f"""
from panda_core_data.model import Model

class TestModel(Model, data_name = "{MODEL_TYPE_NAME}", dependencies = ["{MODEL_TYPE_NAME}",]):
    name: str
    """.strip()

TEMPLATE_FILE = f"""
from panda_core_data.template import Template

class TestTemplate(Template, data_name = "{MODEL_TYPE_NAME}"):
    name: str
""".strip()

INSTANCE_ERROR = "The class wansn't instanced correctly, check __new__ in ModelMixin class"
