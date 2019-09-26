'''
:created: 26-09-2019

:author: Leandro (Cerberus1746) Benedet Garcia
'''
import pytest

from panda_core_data.custom_exceptions import PCDKeyError
from panda_core_data.model import Template


class MappingTemplate(Template):
    name: str
    value: int


TESTING_VALUES = ["test", 10]


def test_mappings():
    second_value = "Another Test"
    instanced = MappingTemplate(*TESTING_VALUES)

    for key_name in instanced:
        assert key_name in ["name", "value"]

    for value in instanced.values():
        assert value in TESTING_VALUES

    for key_name, value in instanced.items():
        assert key_name in ["name", "value"]
        assert value in TESTING_VALUES

    while True:
        try:
            next(instanced)
        except StopIteration:
            break

    instanced["name"] = second_value
    assert instanced.name == second_value
    assert instanced[0] == second_value

    instanced.clear()

    #pylint: disable=len-as-condition
    assert len(instanced) == 0

def test_mapping_exceptions():
    instanced = MappingTemplate(*TESTING_VALUES)
    with pytest.raises(PCDKeyError):
        instanced["invalid"] = "test"

    with pytest.raises(PCDKeyError):
        instanced.pop("invalid")

    with pytest.raises(PCDKeyError):
        #pylint: disable=pointless-statement
        instanced[9]
