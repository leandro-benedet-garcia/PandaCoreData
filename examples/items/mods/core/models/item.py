from panda_core_data.model import Model

class Items(Model, data_name="items", core_name="items"):
    name: str
    description: str
    value: int
