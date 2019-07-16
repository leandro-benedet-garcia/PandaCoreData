'''
:created: 2019-04-30
:author: Leandro (Cerberus1746) Benedet Garcia
'''

from .model_mixin import ModelMixin
from . import data_core, DEFAULT_MODEL_GROUP


class Model(ModelMixin):

    def __init_subclass__(cls, model_name=False, dependency_list=False,  # @NoSelf
                          model_group_name=DEFAULT_MODEL_GROUP):

        cls.model_name = cls.__name__ if not model_name else model_name
        cls.dependencies = [] if not dependency_list else dependency_list
        cls.model_group = model_group_name

        data_core.add_model_type_to_group(model_group_name, cls)

    def setup_values(self, value, default_value, default_min, default_max):
        try:
            current_value = value.get("default_value", None)
            min_value = value.get("default_min", None)
            max_value = value.get("default_max", None)

            if current_value is not None:
                value["max"] = current_value
            elif default_min is not None:
                value["max"] = default_value

            if not max_value is not None:
                value["max"] = max_value
            elif default_min is not None:
                value["max"] = default_max

            if min_value is not None:
                value["max"] = min_value
            elif default_min is not None:
                value["max"] = default_value

        except KeyError as key_not_found:
            raise KeyError(f"Key {key_not_found} not found in {value}"
                           "while trying to setup values.")
        return value

    def initialize_dependencies(self, parent_name):
        current_parent = self.parents[parent_name]
        all_values = current_parent.all()

        if self.parents[parent_name].get_single_value("has_dice_rolls"):
            formated = map(self.calc_dice, all_values)
        else:
            current_value = current_parent.get_single_value("default_value")
            min_value = current_parent.get_single_value("default_min")
            max_value = current_parent.get_single_value("default_max")
            formated = map(lambda x: self.setup_values(
                x, current_value, min_value, max_value), all_values)

        formated = filter(lambda a: not a, formated)
        self.parents[parent_name].purge()
        self.parents[parent_name].insert_multiple(formated)
        return self.parents[parent_name]

    def calc_dice(self, value):
        try:
            if list(value.keys())[0] == "has_dice_rolls":
                value = False
            else:
                value["level"] = self.core.roll_dice(value["dice"])
                value["current_xp"] = value["level"] * value["xp_to_level"]
                if value.get("min_level", False) and value["level"] < value["min_level"]:
                    value["level"] = value["min_level"]

        except KeyError as key_not_found:
            raise KeyError("Key {} not found in {} while trying to roll dices for levels."
                           .format(key_not_found, value))
        return value
