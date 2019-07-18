'''
:created: 2019-04-26
:author: Leandro (Cerberu1746) Benedet Garcia
'''
from . import DEFAULT_MODEL_GROUP, data_core
from .model_mixin import ModelMixin
from .custom_exceptions import CannotInstanceTemplateDirectly


class Template(ModelMixin):
    """
    Class that will be used to make ModelTemplates
    """
    def __new__(cls, *_, **__):
        raise CannotInstanceTemplateDirectly("You can't instantiate a template. They are made "
                                             "to be used just as a dependency for models.")


    def __init_subclass__(cls, template_name=False, # @NoSelf
                          template_group_name=DEFAULT_MODEL_GROUP, auto_create_group=True):
        """
        Method that automatically registers class types into data_core

        :param cls: class type to be added
        :type cls: Model
        :param template_name: The name of the template, if not supplied, the class name is used
        :type template_name: str
        :param template_group_name: Name of the group that the template type will be added. If it \
        doesn't exists, it will be created.
        :type template_group_name: str
        """

        cls.data_name = cls.__name__ if not template_name else template_name
        cls.template_group = template_group_name

        data_core.add_template_to_group(template_group_name, cls, auto_create_group)
