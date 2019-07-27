PandaDataCore
===============

[![Build Status](https://travis-ci.org/Cerberus1746/PandaCoreData.svg?branch=master)](https://travis-ci.org/Cerberus1746/PandaCoreData) [![Documentation Status](https://readthedocs.org/projects/pandacoredata/badge/?version=latest)](https://pandacoredata.readthedocs.io/en/latest/?badge=latest)[![Coverage Status](https://coveralls.io/repos/github/Cerberus1746/PandaCoreData/badge.svg?branch=master)](https://coveralls.io/github/Cerberus1746/PandaCoreData?branch=master)

Thanks for your interest in our package! But for now our things are still a bit of a todo. But, you
can check a basic api documentation here: https://pandacoredata.readthedocs.io/

Install
========

This package only works with python 3.7 and above because it uses dataclasses.

The package is now available with pip, so to install all you need is to run this command:
```
pip install panda-core-data
```

Quick Start
============

Once installed, you can run this command:
```
panda_core_data_commands.py -o directory-name
```
It will automatically generate the basic directory structure, plus a basic main file.

How to Collaborate
=====================

If you want to help with the development of this library, I would say that I love you but my fiancee
 would get jealous, so I will just say thank you :D

First, make sure you have **at least Python 3.7**, git and pip up and running:
```
python -V
pip -V
git --version
```
download this repository with the following command using git:
```
git clone https://github.com/Cerberus1746/PandaCoreData.git
```

And then cd into the directory with:
```
cd PandaCoreData
```

Now, if you want to just run the tests to test your changes, you can run:
```
python setup.py test
```
If you want to generate docs, you can install all dependencies with:
```
pip install panda-core-data[docs]
```

And then generate the docs with the command:
```
python setup.py build_sphinx
```
The docs will be located by default inside the directory `docs/build/html`
