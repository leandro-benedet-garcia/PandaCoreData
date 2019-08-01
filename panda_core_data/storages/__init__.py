from pathlib import Path

from .base_db import available_storages
from .json_db import JsonDB
from .yaml_db import YAMLDB
from ..custom_exceptions import PCDFolderNotFound, PCDFileNotFound, PCDRawFileNotSupported

def get_raw_extensions():
    return [ext for ext_dict in available_storages for ext in ext_dict['extensions']]

def get_extension(path):
    if isinstance(path, Path):
        extension = path.suffix
    elif "\\" in extension or "/" in extension or "." in extension:
        extension = auto_convert_to_pathlib(extension, False).suffix

    return extension.replace(".", "")

def get_storage_from_extension(extension):
    for storage_dict in available_storages:
        if extension in storage_dict["extensions"]:
            return storage_dict["storage"]

    raise PCDRawFileNotSupported(f"The extension {extension} is not supported for raws, the "
                                 f"available extensions are {get_raw_extensions()}")

def raw_glob_iterator(path):
    path = auto_convert_to_pathlib(path, True)
    for ext in get_raw_extensions():
        for file in path.glob(f'*.{ext}'):
            yield file

def is_excluded_extension(path, exclude_ext):
    if exclude_ext and get_extension(path) in exclude_ext:
        return True
    return False

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
