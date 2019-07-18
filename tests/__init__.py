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

INSTANCE_ERROR = "The class wansn't instanced correctly, check __new__ in ModelMixin class"
