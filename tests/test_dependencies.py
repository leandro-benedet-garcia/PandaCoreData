'''
:created: 18-07-2019

:author: Leandro (Cerberus1746) Benedet Garcia
'''
from panda_core_data import data_core
from . import YAML_CONTENT, MODEL_TYPE_NAME

class TestRawLoading(object):
    @staticmethod
    def test_add_dependencies(tmpdir):
        mods_dir = tmpdir.mkdir("mods")
        core_dir = mods_dir.mkdir("core")

        raws_dir = core_dir.mkdir("raws")
        # models_dir = core_dir.mkdir("models")
        # templates_dir = core_dir.mkdir("templates")
        core_dir.mkdir("templates")
        core_dir.mkdir("models")

        raws_dir.join(f"{MODEL_TYPE_NAME}.yaml").write(YAML_CONTENT)

        mods_dir_path = str(mods_dir.realpath())
        data_core(mods_dir_path)
