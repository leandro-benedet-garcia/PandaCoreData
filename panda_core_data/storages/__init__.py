from pathlib import Path

try:
    from .base_db import available_storages
    from .json_db import JsonDB
    from .yaml_db import YamlDB
except ModuleNotFoundError: # pragma: no cover
    print("Tiny Db could not be found")


from ..custom_exceptions import PCDFolderNotFound, PCDFileNotFound, PCDRawFileNotSupported

def get_raw_extensions():
    """
    Get all available extensions the package supports

    :return list(str): A list of available extensions
    """
    return [ext for ext_dict in available_storages for ext in ext_dict['extensions']]

def get_extension(path):
    """
    Get file extension from the path

    :return str: The file extension
    """
    if isinstance(path, Path):
        extension = path.suffix
    elif "\\" in extension or "/" in extension or "." in extension:
        extension = auto_convert_to_pathlib(extension, False).suffix

    return extension.replace(".", "")

def get_storage_from_extension(extension):
    """
    Returns the storage based on the file extension

    :return: Returns a storage object that handles the raw file
    :rtype: :class:`~tinydb.storages.Storage`
    """
    for storage_dict in available_storages:
        if extension in storage_dict["extensions"]:
            return storage_dict["storage"]

    raise PCDRawFileNotSupported(f"The extension {extension} is not supported for raws, the "
                                 f"available extensions are {get_raw_extensions()}")

def raw_glob_iterator(path):
    """
    Iterate along the path yielding the raw file.

    :yields :class:`~pathlib.Path`: The file path
    """
    path = auto_convert_to_pathlib(path, True)
    for ext in get_raw_extensions():
        for file in path.glob(f'*.{ext}'):
            yield file

def is_excluded_extension(path, exclude_ext):
    """
    Check if the file has an ignored extension

    :param path: source folder
    :type path: str or :class:`~pathlib.Path`
    :param list(str) exclude_ext: If the path should be from a folder or file
    :return bool: returns True if it's a excluded extension, False otherwise
    """
    if exclude_ext and get_extension(path) in exclude_ext:
        return True
    return False

def auto_convert_to_pathlib(path, is_folder):
    """
    Check if the path is valid and automatically convert it into a Path object

    :param path: source folder
    :type path: str or :class:`~pathlib.Path`
    :param bool is_folder: If the path should be from a folder or file
    :return: The Path object
    :rtype: :class:`~pathlib.Path`
    :raise PCDFolderNotFound: If the folder is invalid
    :raise PCDFileNotFound: If the file is invalid
    """
    if not isinstance(path, Path):
        path = Path(path)

    if is_folder and not path.is_dir():
        raise PCDFolderNotFound(f"The directory {path} could not be found.")
    elif not is_folder and not path.is_file():
        raise PCDFileNotFound(f"The file {path} could not be found.")

    return path