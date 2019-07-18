'''
Module containing all cusstom exceptions used by the package

:author: Leandro (Cerberus1746) Benedet Garcia
'''


class DataTypeGroupNotFound(Exception):
    """
    Exception raised if the ~Model or ~Template Group is not found.
    """


class DataTypeNotFound(Exception):
    """
    Exception raised if the ~Model or ~Template Group is not found.
    """


class DuplicatedDataTypeName(Exception):
    """
    Exception raised if a ~Model or ~Template Type already exists with the same name inside the
    group.
    """


class FolderNotFound(Exception):
    """
    Exception raised if the folder is invalid.
    """

class CannotInstanceTemplateDirectly(Exception):
    """
    Exception raised if the user attempts to instance a ~Template directly.
    """
