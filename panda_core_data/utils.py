'''
:created: 2019-07-29

:author: Leandro (Cerberus1746) Benedet Garcia
'''
from pathlib import Path
from .custom_exceptions import PCDTypeError, PCDFolderNotFound, PCDFileNotFound

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

def auto_convert_to_pathlib(path, is_folder):
    """
    Check if the path is valid and automatically convert it into a Path object.

    :param path: source folder.
    :type path: str or Path
    :param bool is_folder: If the path should be from a folder or file.
    :return Path: The Path object.
    :raise PCDFolderNotFound: If the folder is invalid.
    :raise PCDFileNotFound: If the file is invalid.
    """
    if not isinstance(path, Path):
        path = Path(path)

    if is_folder and not path.is_dir():
        raise PCDFolderNotFound(f"The directory {path} could not be found.")
    elif not is_folder and not path.is_file():
        raise PCDFileNotFound(f"The file {path} could not be found.")

    return path
