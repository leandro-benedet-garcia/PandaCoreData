'''
Created on Sep 24, 2019

@author: L_BG_
'''
from pathlib import Path
from typing import Union, Mapping, Iterable, List, Dict, Any


PathType = Union[Path, str]
DataDict = List[Dict[str, Any]]

JsonValue = Union[int, str]
JsonMapping = Mapping[str, JsonValue]
JsonTypes = Union[JsonMapping, int, str]
JsonIterable = Iterable[JsonTypes]
JsonInput = Union[str, JsonMapping, JsonIterable]
