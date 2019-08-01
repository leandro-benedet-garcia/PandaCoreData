'''
:created: 2019-07-29

:author: Leandro (Cerberus1746) Benedet Garcia
'''
from .custom_exceptions import PCDTypeError

def check_if_valid_instance(an_object, the_type):
    """
    Check if `an_object` is a instance from `the_type`.

    :param any an_object: source object.
    :param type the_type: type object.
    :raise PCDTypeError: if the type is not a instance or wrong type.
    """
    if not isinstance(an_object, the_type):
        raise PCDTypeError(f"'{an_object}' is not a instance of '{the_type}' or it's not instanced "
                           "at all")
