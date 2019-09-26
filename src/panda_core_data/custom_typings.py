'''
:created: 2019-09-24

@author: Leandro (cerberus1746) Benedet Garcia'''
from pathlib import Path
from typing import Union, Mapping, Iterable, List, Dict, Any


PathType = Union[Path, str]
DataDict = List[Dict[str, Any]]

JsonValue = Union[int, str]
JsonMapping = Mapping[str, JsonValue]
JsonTypes = Union[JsonMapping, int, str]
JsonIterable = Iterable[JsonTypes]
JsonInput = Union[str, JsonMapping, JsonIterable]
