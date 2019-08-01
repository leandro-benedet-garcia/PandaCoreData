'''
:created: 18-07-2019

:author: Leandro (Cerberus1746) Benedet Garcia
'''
import pprint

from panda_core_data import DataCore
from . import (YAML_CONTENT, MODEL_TYPE_NAME, TEMPLATE_TYPE_NAME, MODEL_FILE, TEMPLATE_FILE,
               DEFAULT_TEST_FIELD_NAME, DEFAULT_TEST_FIELD_CONTENT, JSON_CONTENT)

class TestRawLoading(object):
    def dependency_test(self, data_core, file_structure, raw_content, raw_extension):
        pwetty = pprint.PrettyPrinter()
        pwetty.pprint(file_structure)

        core_name = data_core.name
        file_prefix = core_name.title().replace("_", "")
        model_module_name = f"{file_prefix}{MODEL_TYPE_NAME}"
        template_module_name = f"{file_prefix}{TEMPLATE_TYPE_NAME}"
        raw_templates_dir = file_structure["raw_templates_dir"]

        model_content = MODEL_FILE.replace("CORE_NAME", core_name)
        template_content = TEMPLATE_FILE.replace("CORE_NAME", core_name)

        template_file2 = f"""from panda_core_data.model import Template

class TestTemplate2(Template, dependencies=["TestTemplate",], core_name="{core_name}"):
    name: str
        """.strip()

        model_raw = file_structure["model_raw_dir"].join(f"test.{raw_extension}")
        model_raw.write(raw_content)

        raw_template = raw_templates_dir.join(f"{TEMPLATE_TYPE_NAME}.{raw_extension}")
        raw_template2 = raw_templates_dir.join(f"{TEMPLATE_TYPE_NAME}2.{raw_extension}")

        raw_template.write(raw_content)
        raw_template2.write(raw_content)

        file_structure["models_dir"].join(f"{model_module_name}.py").write(model_content)
        file_structure["templates_dir"].join(f"{template_module_name}.py").write(template_content)
        file_structure["templates_dir"].join(f"{template_module_name}2.py").write(template_file2)

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

    def raw_testing(self, data_core, file_structure, raw_content, raw_extension):
        pwetty = pprint.PrettyPrinter()
        pwetty.pprint(file_structure)

        core_name = data_core.name
        file_prefix = core_name.title().replace("_", "")
        model_module_name = f"{file_prefix}{MODEL_TYPE_NAME}.py"
        template_module_name = f"{file_prefix}{TEMPLATE_TYPE_NAME}.py"

        model_content = MODEL_FILE.replace("CORE_NAME", core_name)
        template_content = TEMPLATE_FILE.replace("CORE_NAME", core_name)

        model_raw = file_structure["model_raw_dir"].join(f"test.{raw_extension}")
        model_raw.write(raw_content)

        raw_template = file_structure["raw_templates_dir"].join(f"{TEMPLATE_TYPE_NAME}."
                                                                f"{raw_extension}")
        raw_template.write(raw_content)

        file_structure["models_dir"].join(model_module_name).write(model_content)
        file_structure["templates_dir"].join(template_module_name).write(template_content)

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

    def test_load_yaml_types(self, file_structure):
        core_name = "test_load_yaml_types"
        data_core = DataCore(name=core_name)

        self.raw_testing(data_core, file_structure, YAML_CONTENT, "yaml")


    def test_load_json_types(self, file_structure):
        core_name = "test_load_json_types"
        data_core = DataCore(name=core_name)

        self.raw_testing(data_core, file_structure, JSON_CONTENT, "json")

    def test_inner_dependencies_yaml(self, file_structure):
        core_name = "test_inner_dependencies_yaml"
        data_core = DataCore(name=core_name)

        self.dependency_test(data_core, file_structure, YAML_CONTENT, "yaml")

    def test_inner_dependencies_json(self, file_structure):
        core_name = "test_inner_dependencies_json"
        data_core = DataCore(name=core_name)

        self.dependency_test(data_core, file_structure, JSON_CONTENT, "json")
