'''
:created: 2019-09-20

:author: Leandro (Cerberus1746) Benedet Garcia
'''
from typing import Callable, Optional
from .custom_typings import JsonInput


class DataTypeGenerator(): #pylint: disable=too-few-public-methods
    def __init__(self, name: str, json_input: JsonInput,
                 decode_callable: Optional[Callable] = None):
        pass
