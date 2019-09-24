'''
:created: 03-08-2019

:author: Leandro (Cerberus1746) Benedet Garcia
'''
from panda_core_data import DataCore
from panda_core_data.model import Model


class TestGeneral():
    #pylint: disable=unused-argument
    @staticmethod
    def writing_method_test(file_structure, data_core, raw_file,
                            extension):
        model_raw = file_structure["model_raw_dir"].join(f"test.{extension}")
        model_raw.write(raw_file)

        class WriteTest(Model, core_name=data_core.name):
            name: str
            description: str
            value: int

        instance = WriteTest.instance_from_raw(model_raw.realpath())

        instance.name = "Iron"
        instance.description = "Basic material"

        instance.save_to_file()

        instance = WriteTest.instance_from_raw(model_raw.realpath())

        assert instance.name == "Iron"
        assert instance.description == "Basic material"
        assert instance.value == 1

    def test_json_write(self, file_structure):
        data_core = DataCore(name="test_json_write")

        raw_file = """
        {"data": [
            {"name": "Copper"},
            {"description": "Fragile material"},
            {"value": 1}
        ]}
        """.strip()

        self.writing_method_test(file_structure, data_core, raw_file, "json")

    def test_yaml_write(self, file_structure):
        data_core = DataCore(name="test_yaml_write")

        raw_file = """
        data:
        - name: Copper
        - description: Fragile material
        - value: 1
        """.strip()

        self.writing_method_test(file_structure, data_core, raw_file, "yaml")
