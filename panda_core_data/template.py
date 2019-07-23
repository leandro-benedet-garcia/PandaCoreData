'''
:created: 2019-04-26
:author: Leandro (Cerberu1746) Benedet Garcia
'''
from . import data_core
from .model_mixin import ModelMixin


class Template(ModelMixin):
    """
    Class that will be used to make ModelTemplates
    """

    def __init_subclass__(cls, **kwargs):  # @NoSelf
        """
        Method that automatically registers class types into data_core

        :param cls: class type to be added
        :type cls: Model
        :param template_name: The name of the template, if not supplied, the class name is used
        :type template_name: str
        :param template_group_name: Name of the group that the template type will be added. If it \
        doesn't exists, it will be created.
        :param dependency_list: TODO
        :type dependency_list: list of strings
        :type template_group_name: str
        """

        cls._add_into(cls, data_core.all_key_value_templates, # @UndefinedVariable
                      data_core.get_template_group, # @UndefinedVariable
                      data_core.get_or_create_template_group, **kwargs) # @UndefinedVariable
