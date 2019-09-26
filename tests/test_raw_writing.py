'''
:created: 03-08-2019

:author: Leandro (Cerberus1746) Benedet Garcia
'''
from panda_core_data import DataCore
from panda_core_data.model import Model

#pylint: disable=unused-argument
def writing_method_test(file_structure, data_core, raw_file, extension):
    model_raw = file_structure["model_raw_dir"].join(f"test.{extension}")
    model_raw.write(raw_file)

    full_model_path = model_raw.realpath()

    class WriteTest(Model, core_name=data_core.name):
        name: str
        description: str
        value: int

    with WriteTest.instance_from_raw(full_model_path) as instance:
        instance.name = "Iron"
        instance.description = "Basic material"

    instance = WriteTest.instance_from_raw(full_model_path)

    assert instance.name == "Iron"
    assert instance.description == "Basic material"
    assert instance.value == 1

def test_json_write(file_structure):
    data_core = DataCore(name="test_json_write")

    raw_file = """
    {"data": [
        {"name": "Copper"},
        {"description": "Fragile material"},
        {"value": 1}
    ]}
    """.strip()

    writing_method_test(file_structure, data_core, raw_file, "json")

def test_yaml_write(file_structure):
    data_core = DataCore(name="test_yaml_write")

    raw_file = """
    data:
    - name: Copper
    - description: Fragile material
    - value: 1
    """.strip()

    writing_method_test(file_structure, data_core, raw_file, "yaml")
