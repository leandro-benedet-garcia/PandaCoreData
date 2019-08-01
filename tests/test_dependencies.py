'''
:created: 18-07-2019

:author: Leandro (Cerberus1746) Benedet Garcia
'''
import pprint

from panda_core_data import DataCore
from . import (YAML_CONTENT, MODEL_TYPE_NAME, TEMPLATE_TYPE_NAME, MODEL_FILE, TEMPLATE_FILE,
               DEFAULT_TEST_FIELD_NAME, DEFAULT_TEST_FIELD_CONTENT, JSON_CONTENT)

class TestRawLoading(object):
    @staticmethod
    def test_load_yaml_types(file_structure):
        core_name = "test_load_yaml_types"

        data_core = DataCore(name=core_name)
        model_content = MODEL_FILE.replace("CORE_NAME", core_name)
        template_content = TEMPLATE_FILE.replace("CORE_NAME", core_name)

        model_raw = file_structure["model_raw_dir"].join(f"test.yaml")
        model_raw.write(YAML_CONTENT)

        raw_template = file_structure["raw_templates_dir"].join(f"{TEMPLATE_TYPE_NAME}.yaml")
        raw_template.write(YAML_CONTENT)

        file_structure["models_dir"].join(f"{MODEL_TYPE_NAME}.py").write(model_content)
        file_structure["templates_dir"].join(f"{TEMPLATE_TYPE_NAME}.py").write(template_content)

        data_core(file_structure["mods_dir"].realpath())

        assert len(list(data_core.all_template_instances)) == 1
        assert len(list(data_core.all_model_instances)) == 1

        for current_model_instance in data_core.all_model_instances:
            for template_instance in data_core.all_template_instances:
                template_name = template_instance.data_name
                model_parent = current_model_instance.parents.get(template_name)
                field_content = getattr(template_instance, DEFAULT_TEST_FIELD_NAME)

                assert model_parent == template_instance
                assert field_content == DEFAULT_TEST_FIELD_CONTENT

    @staticmethod
    def test_load_json_types(file_structure):
        pwetty = pprint.PrettyPrinter()
        pwetty.pprint(file_structure)
        core_name = "test_load_json_types"

        data_core = DataCore(name=core_name)
        model_content = MODEL_FILE.replace("CORE_NAME", core_name)
        template_content = TEMPLATE_FILE.replace("CORE_NAME", core_name)

        model_raw = file_structure["model_raw_dir"].join(f"test.json")
        model_raw.write(JSON_CONTENT)

        raw_template = file_structure["raw_templates_dir"].join(f"{TEMPLATE_TYPE_NAME}.json")
        raw_template.write(JSON_CONTENT)

        file_structure["models_dir"].join(f"{MODEL_TYPE_NAME}.py").write(model_content)
        file_structure["templates_dir"].join(f"{TEMPLATE_TYPE_NAME}.py").write(template_content)

        data_core(file_structure["mods_dir"].realpath())

        assert len(list(data_core.all_template_instances)) == 1
        assert len(list(data_core.all_model_instances)) == 1

        for current_model_instance in data_core.all_model_instances:
            for template_instance in data_core.all_template_instances:
                template_name = template_instance.data_name
                model_parent = current_model_instance.parents.get(template_name)
                field_content = getattr(template_instance, DEFAULT_TEST_FIELD_NAME)

                assert model_parent == template_instance
                assert field_content == DEFAULT_TEST_FIELD_CONTENT

    @staticmethod
    def test_inner_dependencies(file_structure):
        pwetty = pprint.PrettyPrinter()
        pwetty.pprint(file_structure)
        core_name = "test_inner_dependencies"

        data_core = DataCore(name=core_name)
        model_content = MODEL_FILE.replace("CORE_NAME", core_name)
        template_content = TEMPLATE_FILE.replace("CORE_NAME", core_name)

        template_file2 = """from panda_core_data.model import Template

class TestTemplate2(Template, data_name="TestTemplate2",
                    dependencies=["TestTemplate",], core_name="test_inner_dependencies"):
    name: str
        """.strip()

        model_raw = file_structure["model_raw_dir"].join(f"test.yaml")
        model_raw.write(YAML_CONTENT)

        raw_template = file_structure["raw_templates_dir"].join(f"{TEMPLATE_TYPE_NAME}.yaml")
        raw_template2 = file_structure["raw_templates_dir"].join(f"{TEMPLATE_TYPE_NAME}2.yaml")

        raw_template.write(YAML_CONTENT)
        raw_template2.write(YAML_CONTENT)

        file_structure["models_dir"].join(f"test_model.py").write(model_content)
        file_structure["templates_dir"].join(f"test_template.py").write(template_content)
        file_structure["templates_dir"].join(f"test_template2.py").write(template_file2)

        assert len(data_core.recursively_add_module(file_structure["models_dir"])) == 1
        assert len(data_core.recursively_add_module(file_structure["templates_dir"])) == 2

        data_core.recursively_instance_template(file_structure["raw_templates_dir"])
        pwetty.pprint(list(data_core.all_template_instances))
        assert len(list(data_core.all_template_instances)) == 2

        data_core.recursively_instance_model(file_structure["root_model_raw_dir"])
        pwetty.pprint(list(data_core.all_model_instances))
        assert len(list(data_core.all_model_instances)) == 1

        for current_instance in data_core.all_model_instances:
            if current_instance.has_dependencies:
                current_instance.add_dependencies()

        print("Final Output: " + str(list(data_core.all_model_instances)))
