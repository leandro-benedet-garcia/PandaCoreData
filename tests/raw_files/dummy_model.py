# pylint: skip-file
from panda_core_data.model import Model

class MODEL_TYPE_NAME(Model, data_name="MODEL_TYPE_NAME",
                      dependencies=["TEMPLATE_TYPE_NAME",],
                      core_name="CORE_NAME"):
    name: str
