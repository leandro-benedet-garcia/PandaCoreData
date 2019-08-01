'''
Module containing all cusstom exceptions used by the package. All exceptions related to this package
has the PCD prefix.

Please, if you used one of our methods and it raised an exception that doesn't have our PCD prefix
**and** it came from inside our files send us a ticket in this link:
https://github.com/Cerberus1746/PandaCoreData/issues

:author: Leandro (Cerberus1746) Benedet Garcia
'''

class PCDDuplicatedTypeName(Exception):
    """
    Exception raised if a :class:`~panda_core_data.models.Model` or \
    :class:`~panda_core_data.models.Template` Type already exists with the same name.
    """

class PCDFolderNotFound(Exception):
    """Exception raised if the folder is invalid."""

class PCDFileNotFound(PCDFolderNotFound):
    """Exception raised if the file is invalid."""

class PCDFolderIsEmpty(PCDFolderNotFound):
    """Exception raised if the folder is empty."""

class PCDDataCoreIsNotUnique(Exception):
    """Exception raised if the data core is not unique."""

class PCDInvalidRaw(Exception):
    """Exception raised if a raw is invalid"""

class PCDDuplicatedModuleName(Exception):
    """Exception raised if a module with the same name was already imported"""

class PCDTypeError(TypeError):
    """Exception raised if a invalid type was found."""

class PCDInvalidPathType(KeyError):
    """Exception raised if a invalid folder type was requested."""

class PCDInvalidBaseData(TypeError):
    """Exception raised if a base doesn't have a method."""

class PCDRawFileNotSupported(Exception):
    """Exception raised if the package can't read the extension."""
