PandaDataCore
===============

[![Build Status](https://travis-ci.org/Cerberus1746/PandaCoreData.svg?branch=master)](https://travis-ci.org/Cerberus1746/PandaCoreData) [![Documentation Status](https://readthedocs.org/projects/pandacoredata/badge/?version=latest)](https://pandacoredata.readthedocs.io/en/latest/?badge=latest)[![Coverage Status](https://coveralls.io/repos/github/Cerberus1746/PandaCoreData/badge.svg?branch=master)](https://coveralls.io/github/Cerberus1746/PandaCoreData?branch=master)

Thanks for your interest in our package! But for now our things are still a bit of a todo. But, you
can check a basic api documentation here: https://pandacoredata.readthedocs.io/

How to Collaborate
=====================

If you want to help with the development of this library, I would say that I love you but my fiancee
 would get jealous, so I will just say thank you :D

First, make sure you have **at least Python 3.7**, git and pip up and running:
```
python -V #it **must** show a version that is at least 3.7 otherwise something is wrong.
pip -V
git --version
```
download this repository with the following command using git:
```git clone https://github.com/Cerberus1746/PandaCoreData.git```

And then cd into the directory with:
```cd PandaCoreData```

Now, if you want to just run the tests to test your changes, you can run:
```python setup.py test```

This will get all dependencies for that to happen. But if you want to install all the things into
 your computer. Follow one of those instructions.

Pipenv install
---------------

To install with pipenv you can just run this command:

```pip install pipenv
pipenv install```

This will install and make pipenv download all you need to generate the docs and to run the test
script files in addition to creating a virtual env for you, in two commands (if you install it
first).

To use the virtualenv that you made with pipenv, simply use:

```pipenv shell```

Using a virtual env
---------------------

To create a virtualenv manually and install everything you need in it:
```pip install virtualenv
virtualenv panda_core_data
source panda_core_data/bin/activate
cd panda_core_data
pip install -r requirements.txt```

Remember that to generate docs and run tests you will need to run

```source panda_core_data/bin/activate```

To activate the virtual env

Just install globally
-------------------------
or, to just install globally in your computer (which I don't recomend)

```pip install -r requirements.txt```

Using installed packages
=========================

All the following commands assumes you have your virtualenv active. Either with pipenv or
normal virtualenv

To run all the tests to make sure your changes didn't break anything and the code is formatted
correctly:
```pytest tests/ --pylint```

And to generate the docs:
```./docs/make # .\docs\make.bat if you are using windows.```
