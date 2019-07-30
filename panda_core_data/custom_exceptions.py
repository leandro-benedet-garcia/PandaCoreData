'''
Module containing all cusstom exceptions used by the package. All exceptions related to this package
has the PCD prefix.

Please, if you used one of our methods and it raised an exception that doesn't have our PCD prefix
**and** it came from inside our files send us a ticket in this link:
https://github.com/Cerberus1746/PandaCoreData/issues

:author: Leandro (Cerberus1746) Benedet Garcia
'''

class PCDTypeNotFound(Exception):
    """Exception raised if the ~Model or ~Template Group is not found."""


class PCDDuplicatedTypeName(Exception):
    """
    Exception raised if a ~Model or ~Template Type already exists with the same name inside the
    group.
    """

class PCDFolderNotFound(Exception):
    """Exception raised if the folder is invalid."""

class PCDFileNotFound(PCDFolderNotFound):
    """Exception raised if the file is invalid."""

class PCDFolderIsEmpty(PCDFolderNotFound):
    """Exception raised if the folder is empty."""

class PCDDataCoreIsNotUnique(Exception):
    """Exception raised if the data core is not unique."""

class PCDTypeError(TypeError):
    pass

class PCDInvalidPathType(KeyError):
    """Exception raised if a invalid folder type was requested."""

class PCDInvalidBaseData(TypeError):
    """Exception raised if a base doesn't have a method."""
