'''
Module containing all custom exceptions used by the package. All exceptions related to this package
has the PCD prefix.

Please, if you used one of our methods and it raised an exception that doesn't have our PCD prefix
**and** it came from inside our files send us a ticket in this link:
https://github.com/Cerberus1746/PandaCoreData/issues

:author: Leandro (Cerberus1746) Benedet Garcia
'''
class PCDException(Exception):
    """
    Parent exception for all other exceptions
    """

class PCDDuplicatedTypeName(PCDException):
    """
    Exception raised if a :class:`~panda_core_data.models.Model` or
    :class:`~panda_core_data.models.Template` Type already exists with the same name.
    """

class PCDInvalidPath(PCDException):
    """Exception raised if the file is invalid."""

class PCDFolderIsEmpty(PCDInvalidPath):
    """Exception raised if the folder is empty."""

class PCDDataCoreIsNotUnique(PCDException):
    """Exception raised if the data core is not unique."""

class PCDInvalidRaw(PCDException):
    """Exception raised if a raw is invalid"""

class PCDDuplicatedModuleName(PCDException):
    """Exception raised if a module with the same name was already imported"""

class PCDTypeError(TypeError, PCDException):
    """Exception raised if a invalid type was found."""

class PCDInvalidPathType(KeyError, PCDException):
    """Exception raised if a invalid path type was requested."""

class PCDInvalidBaseData(PCDTypeError):
    """Exception raised if a base doesn't have a method."""

class PCDRawFileNotSupported(PCDTypeError):
    """Exception raised if the package can't read the extension."""
