'''
:author: Leandro (Cerberus1746) Benedet Garcia
'''
try:
    from sphinx.setup_command import BuildDoc
    SPHINX_LOADED = True
except(ModuleNotFoundError, ImportError):
    SPHINX_LOADED = False

import setuptools
from panda_core_data.__version__ import __version__
if SPHINX_LOADED:
    CMDCLASS = {'build_sphinx': BuildDoc}

NAME = 'panda_core_data'

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

with open("LICENSE", "r") as fh:
    LICENSE = fh.read()

with open("requirements.txt", "r") as fh:
    REQUIREMENTS = fh.read().strip().split("\n")

with open("requirements-tests.txt", "r") as fh:
    TEST_PACKAGES = fh.read().strip().split("\n")

with open("requirements-docs.txt", "r") as fh:
    REQUIREMENTS_DOCS = fh.read().strip().split("\n")

setuptools.setup(
    name=NAME,
    version=__version__,
    cmdclass=CMDCLASS if SPHINX_LOADED else {},
    author="Leandro (Cerberus1746) Benedet Garcia",
    author_email="leandro.benedet.garcia@gmail.com",
    description="Data management system with modding and Panda3D engine in mind.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    license="MIT License",
    python_requires=">=3.7",
    url="https://github.com/Cerberus1746/PandaCoreData",
    tests_require=TEST_PACKAGES,
    packages=["panda_core_data", "panda_core_data.data_core_bases", "panda_core_data.storages"],
    setup_requires=['pytest-runner'],
    scripts=['scripts/panda_core_data_commands.py'],
    extras_require={
        'tests': TEST_PACKAGES,
        'docs': REQUIREMENTS_DOCS
    },
    install_requires=REQUIREMENTS,
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",

        "License :: OSI Approved :: MIT License",

        "Operating System :: OS Independent",

        "Development Status :: 2 - Pre-Alpha",

        "Intended Audience :: Developers",

        "Topic :: Games/Entertainment",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
    ],
    command_options={
        'build_sphinx': {
            'project': ('setup.py', NAME),
            'version': ('setup.py', __version__),
            'source_dir': ('setup.py', 'docs/source'),
            'build_dir': ('setup.py', 'docs/build'),
        }
    } if SPHINX_LOADED else {},
)
