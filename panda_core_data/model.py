'''
:created: 2019-04-30
:author: Leandro (Cerberus1746) Benedet Garcia
'''

from panda_core_data.data_type import DataType

class Template(DataType):
    """
    Class that will be used to make ModelTemplates
    """

    def __init_subclass__(cls, core_name=None, **kwargs):  # @NoSelf
        """
        Method that automatically registers class types into data_core. You can use the same
        parameters as :meth:`~panda_core_data.data_type.DataType._add_into`
        """
        current_core = cls._get_core(core_name)
        cls.data_core = current_core

        cls._add_into(cls, current_core.all_key_value_templates, **kwargs)

    @classmethod
    def instanced(cls):
        return cls.wrapper.instances

class ModelIter(type):
    #pylint: disable=non-iterator-returned
    def __iter__(cls):  # @NoSelf
        return cls.all_instances

    @property
    def all_instances(cls):  # @NoSelf
        return iter(cls.wrapper.instances)


class Model(DataType, metaclass=ModelIter):
    def __init_subclass__(cls, core_name=None, **kwargs):  # @NoSelf
        """
        Method that automatically registers class types into data_core. You can use the same
        parameters as :meth:`~panda_core_data.data_type.DataType._add_into`
        """
        current_core = cls._get_core(core_name)
        cls.data_core = current_core
        cls._add_into(cls, current_core.all_model_types, **kwargs)

    #def setup_values(self, value, default_value, default_min, default_max):
    #    try:
    #        current_value = value.get("default_value", None)
    #        min_value = value.get("default_min", None)
    #        max_value = value.get("default_max", None)

    #        if current_value is not None:
    #            value["max"] = current_value
    #        elif default_min is not None:
    #            value["max"] = default_value

    #        if not max_value is not None:
    #            value["max"] = max_value
    #        elif default_min is not None:
    #            value["max"] = default_max

    #        if min_value is not None:
    #            value["max"] = min_value
    #        elif default_min is not None:
    #            value["max"] = default_value

    #    except KeyError as key_not_found:
    #        raise KeyError(f"Key {key_not_found} not found in {value}"
    #                       "while trying to setup values.")
    #    return value

    #def initialize_dependencies(self, parent_name):
    #    """
    #    :param str parent_name: name of the template to be instanced.
    #    """
    #    current_parent = self.parents[parent_name]
    #    all_values = current_parent.all()

    #    if self.parents[parent_name].get_single_value("has_dice_rolls"):
    #        formated = map(self.calc_dice, all_values)
    #    else:
    #        current_value = current_parent.get_single_value("default_value")
    #        min_value = current_parent.get_single_value("default_min")
    #        max_value = current_parent.get_single_value("default_max")
    #        formated = map(lambda x: self.setup_values(x, current_value, min_value, max_value),
    #                       all_values)

    #    formated = filter(lambda a: not a, formated)
    #    self.parents[parent_name].purge()
    #    self.parents[parent_name].insert_multiple(formated)
    #    return self.parents[parent_name]
