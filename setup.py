'''
:author: Leandro (Cerberus1746) Benedet Garcia
'''

import setuptools

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name='panda_core_data',
    version='0.0.1.dev1',
    author="Leandro (Cerberus1746) Benedet Garcia",
    author_email="leandro.benedet.garcia@gmail.com",
    description="Data management system with modding and Panda3D engine in mind.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/Cerberus1746/PandaCoreData",
    packages=setuptools.find_packages(),
    setup_requires=[
        'pytest-runner'
    ],
    tests_require=[
        'pytest',
        'pylint',
        'pytest-pylint',
        'python-coveralls',
    ],
    install_requires=[
        "tinydb",
        "pyyaml",
    ],
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
)
