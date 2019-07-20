#===================================================================================================
# '''
# :created: 18-07-2019
#
# :author: Leandro (Cerberus1746) Benedet Garcia
# '''
# from panda_core_data import data_core
# from . import YAML_CONTENT, MODEL_TYPE_NAME
#
# class TestRawLoading(object):
#     model_file = f"""
# from panda_core_data.model import Model
#
# class TestModel(Model, model_name = "{MODEL_TYPE_NAME}", dependencies = ["{MODEL_TYPE_NAME}",]):
#     name: str
#     """.strip()
#
#     template_file = f"""
# from panda_core_data.template import Template
#
# class TestTemplate(Template, template_name = "{MODEL_TYPE_NAME}"):
#     name: str
#     """.strip()
#
#     def test_load_types(self, tmpdir):
#         mods_dir = tmpdir.mkdir("mods")
#         core_dir = mods_dir.mkdir("core")
#
#         models_dir = core_dir.mkdir("models")
#         templates_dir = core_dir.mkdir("templates")
#
#         raws_dir = core_dir.mkdir("raws")
#         raw_models_dir = raws_dir.mkdir("models")
#         raw_templates_dir = raws_dir.mkdir("templates")
#
#         raw_models_dir.join(f"{MODEL_TYPE_NAME}.yaml").write(YAML_CONTENT)
#         raw_templates_dir.join(f"{MODEL_TYPE_NAME}.yaml").write(YAML_CONTENT)
#
#         models_dir.join(f"{MODEL_TYPE_NAME}.py").write(self.model_file)
#         templates_dir.join(f"{MODEL_TYPE_NAME}.py").write(self.template_file)
#
#         mods_dir_path = str(mods_dir.realpath())
#         data_core(mods_dir_path)
#===================================================================================================
