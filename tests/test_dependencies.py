'''
:created: 18-07-2019

:author: Leandro (Cerberus1746) Benedet Garcia
'''
from panda_core_data import data_core
from . import (YAML_CONTENT, MODEL_TYPE_NAME, TEMPLATE_TYPE_NAME, MODEL_FILE, TEMPLATE_FILE,
               DEFAULT_TEST_FIELD_NAME)

class TestRawLoading(object):
    @staticmethod
    def test_load_types(tmpdir, template):
        mods_dir = tmpdir.mkdir("mods")
        core_dir = mods_dir.mkdir("core")

        models_dir = core_dir.mkdir("models")
        templates_dir = core_dir.mkdir("templates")

        raws_dir = core_dir.mkdir("raws")
        raw_models_dir = raws_dir.mkdir("models")
        raw_templates_dir = raws_dir.mkdir("templates")

        raw_models_dir.join(f"{MODEL_TYPE_NAME}.yaml").write(YAML_CONTENT)

        raw_template = raw_templates_dir.join(f"{TEMPLATE_TYPE_NAME}.yaml")
        raw_template.write(YAML_CONTENT)

        models_dir.join(f"{MODEL_TYPE_NAME}.py").write(MODEL_FILE)
        templates_dir.join(f"{TEMPLATE_TYPE_NAME}.py").write(TEMPLATE_FILE)

        mods_dir_path = str(mods_dir.realpath())

        test_instance = template.instance_from_raw(raw_template.realpath())
        test_field_value = getattr(test_instance, DEFAULT_TEST_FIELD_NAME)

        data_core(mods_dir_path)
        for current_model_instance in data_core.get_model_instances():
            for template_instance in data_core.get_template_instances():
                template_name = template_instance.data_name
                model_parent = current_model_instance.parents.get(template_name)
                assert model_parent == template_instance
                assert getattr(template_instance, DEFAULT_TEST_FIELD_NAME) == test_field_value
