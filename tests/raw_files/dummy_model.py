from panda_core_data.model import Model

class MODEL_TYPE_NAME(Model, dependencies=["TEMPLATE_TYPE_NAME",]):
    name: str
