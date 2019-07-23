'''
:created: 18-07-2019

:author: Leandro (Cerberus1746) Benedet Garcia
'''
from panda_core_data import data_core
from . import YAML_CONTENT, MODEL_TYPE_NAME, TEMPLATE_TYPE_NAME, MODEL_FILE, TEMPLATE_FILE

class TestRawLoading(object):
    @staticmethod
    def test_load_types(tmpdir):
        mods_dir = tmpdir.mkdir("mods")
        core_dir = mods_dir.mkdir("core")

        models_dir = core_dir.mkdir("models")
        templates_dir = core_dir.mkdir("templates")

        raws_dir = core_dir.mkdir("raws")
        raw_models_dir = raws_dir.mkdir("models")
        raw_templates_dir = raws_dir.mkdir("templates")

        raw_models_dir.join(f"{MODEL_TYPE_NAME}.yaml").write(YAML_CONTENT)
        raw_templates_dir.join(f"{TEMPLATE_TYPE_NAME}.yaml").write(YAML_CONTENT)

        models_dir.join(f"{MODEL_TYPE_NAME}.py").write(MODEL_FILE)
        templates_dir.join(f"{TEMPLATE_TYPE_NAME}.py").write(TEMPLATE_FILE)

        mods_dir_path = str(mods_dir.realpath())

        for variable in locals().values():
            if hasattr(variable, "realpath"):
                print(variable.realpath())
        data_core(mods_dir_path)
