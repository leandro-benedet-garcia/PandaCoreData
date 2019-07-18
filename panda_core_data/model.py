'''
:created: 2019-04-30
:author: Leandro (Cerberus1746) Benedet Garcia
'''

from .model_mixin import ModelMixin
from . import data_core, DEFAULT_MODEL_GROUP


class Model(ModelMixin):

    def __init_subclass__(cls, model_name=False, dependency_list=False,  # @NoSelf
                          model_group_name=DEFAULT_MODEL_GROUP, auto_create_group=True):
        """
        Method that automatically registers class types into data_core

        :param cls: class type to be added
        :type cls: Model
        :param model_name: The name of the model, if not supplied, the class name is used
        :type model_name: str
        :param dependency_list: TODO
        :type dependency_list: list of strings
        :param model_group_name: Name of the group that the model type will be added. If it \
        doesn't exists, it will be created.
        :type model_group_name: str
        """

        cls.data_name = cls.__name__ if not model_name else model_name
        cls.dependencies = [] if not dependency_list else dependency_list
        cls.model_group = model_group_name

        data_core.add_model_to_group(model_group_name, cls, auto_create_group)

    #def setup_values(self, value, default_value, default_min, default_max):
    #    try:
    #        current_value = value.get("default_value", None)
    #        min_value = value.get("default_min", None)
    #        max_value = value.get("default_max", None)
    #
    #        if current_value is not None:
    #            value["max"] = current_value
    #        elif default_min is not None:
    #            value["max"] = default_value
    #
    #        if not max_value is not None:
    #            value["max"] = max_value
    #        elif default_min is not None:
    #            value["max"] = default_max
    #
    #        if min_value is not None:
    #            value["max"] = min_value
    #        elif default_min is not None:
    #            value["max"] = default_value
    #
    #    except KeyError as key_not_found:
    #        raise KeyError(f"Key {key_not_found} not found in {value}"
    #                       "while trying to setup values.")
    #    return value

    #def initialize_dependencies(self, parent_name):
    #    """
    #    :todo: make it work again.
    #    :param parent_name: name of the template to be instanced.
    #    :type parent_name: str
    #    """
    #    current_parent = self.parents[parent_name]
    #    all_values = current_parent.all()
    #
    #    if self.parents[parent_name].get_single_value("has_dice_rolls"):
    #        formated = map(self.calc_dice, all_values)
    #    else:
    #        current_value = current_parent.get_single_value("default_value")
    #        min_value = current_parent.get_single_value("default_min")
    #        max_value = current_parent.get_single_value("default_max")
    #        formated = map(lambda x: self.setup_values(
    #            x, current_value, min_value, max_value), all_values)

    #    formated = filter(lambda a: not a, formated)
    #    self.parents[parent_name].purge()
    #    self.parents[parent_name].insert_multiple(formated)
    #    return self.parents[parent_name]
