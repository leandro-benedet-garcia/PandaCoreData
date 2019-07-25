from os.path import join, abspath, dirname

def read_and_replace(file_name):
    with open(join(abspath(dirname(__file__)), "raw_files", file_name), "r") as file_rh:
        file_contents = str(file_rh.read())
        for var_name, value in globals().items():
            if value and isinstance(value, str):
                file_contents = file_contents.replace(var_name, value)

    return file_contents

MODEL_TYPE_NAME = "TestModel"
TEMPLATE_TYPE_NAME = "TestTemplate"
SECOND_MODEL_TYPE_NAME = "second_model_type_name"
MODEL_WITH_INIT_NAME = "model_with_init_name"
CREATION_TEST_NAME = "creation_test_name"

DEFAULT_TEST_FIELD_NAME = "name"
DEFAULT_TEST_FIELD_CONTENT = "name_content"

INSTANCE_ERROR = "The class wansn't instanced correctly, check __new__ in ModelMixin class"

YAML_CONTENT = read_and_replace("test.yaml")
MODEL_FILE = read_and_replace("dummy_model.py")
TEMPLATE_FILE = read_and_replace("dummy_template.py")
