class ModelTypeGroupNotFound(Exception):
	"""
	Exception raised if the Model Type Group is not found.
	"""

class ModelTypeNotFound(Exception):
	"""
	Exception raised if the Model Group is not found.
	"""

class DuplicatedModelTypeName(Exception):
	"""
	Exception raised if a Model Type already exists with the same name inside the group.
	"""

class FolderNotFound(Exception):
	"""
	Exception raised if the folder is invalid.
	"""
