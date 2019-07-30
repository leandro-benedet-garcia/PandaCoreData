.. contents ::

################
Getting Started
################
First of all we need to install the library so we can use it! So here we go:

*************
Installation
*************
Python have a lot of options if you want to install a package. Since the library is available in
Pypi repository all you need to run most of the time is:

.. code:: bash

    pip install panda_core_data

That command should work with Windows, Mac or Linux.

************
Quick Start
************
Once installed, the following command is available:

.. code:: bash

    panda_core_data_commands -o folder_name

Which will create all the necessary folder structure and a example
:class:`~panda_core_data.model.Model` together with their raws inside the supplied `folder_name`.

***********
Data Types
***********
The library has mostly 4 types of data structures, :class:`~panda_core_data.model.Model` and
:class:`~panda_core_data.model.Template`, and then we have
their raw files being *raw templates* and *raw models*.

Once you create a class and inherit a :class:`~panda_core_data.model.Model` or
:class:`~panda_core_data.model.Template`, the class is automatically transformed into a
`dataclass <https://docs.python.org/3/library/dataclasses.html>`_.

Models
^^^^^^^
Models are pretty much what you will use inside your game to use the data. You can instance
multiple times :class:`~panda_core_data.model.Model` classes each containing a different set of
data and accessing them based on how you created the model. But by default you set the fields like
you do with a `dataclass` and  the automatic finders will create a model instance with the data
from the raw.

For learning purposes. Let's consider you executed the `quick start command <#quick-start>`_
with the folder named `tutorial`. Then go to the file
`/tutorial/mods/core/models/example_model.py` rename however you like and write it like this:

.. code:: python

    from panda_core_data.model import Model

    class Items(Model, data_name="items"):
        name: str
        description: str
        cost: int

Mostly, we are just setting the `data_name` parameter to make the **I** in low caps there's more
parameters in :meth:`~panda_core_data.data_type.DataType.__add_into`. Also remember, if you inherit
:class:`~panda_core_data.model.Template` or :class:`~panda_core_data.model.Model`, the class will
turn into a dataclass, so you can instance the model like this for example:

.. code:: python

    Items("Copper", "Fragile material", 1) # The args are in the field order
    Items(name="Copper", description="Fragile material", cost=1) # as kwargs

But that's not the point of our library, the point is to have easy way to load data from raw
files. So let's go to the folder `/tutorial/mods/core/raws/models/` and rename the folder
`model_name` to the name of your model which in our current case is `items` if you didn't set the
param `data_name` the model name will be `Items` with a capital **I** because the library will set
the same name as the class.

Since models can be instanced multiple times, it will read all raw files inside the folder that
have the same name as the model (if it's inside the folder `/mods/core/raws/models/` in this case)
and load a instance with the data of the raw.

Raws
^^^^^
The raws are pretty much plain text files that holds data for our instances. For now we only
support the format yaml but soon support for xml and json will be added.

So let's go to the file `/tutorial/mods/core/raws/models/items/example_model_raw.yaml` rename it to
whatever name you'd like, for the tutorial let's name it `copper.yaml` and set it's contents to:

.. code:: yaml

    data:
        - name: "Copper"
        - description: "Fragile material"
        - value: 1

And the data of our instance will be the same as the above.

To load the raw you can do like this:

.. code:: python

    copper = Items.instance_from_raw("/tutorial/mods/core/raws/models/items/copper.yaml")

Needless to say you need to fix the path to the file. Because I'm not in your computer and I don't
know if you use gentoo with a custom kernel having the root folder named `popcorn` (I don't even
know if it's possible to change the root folder, but if I could I would totally name it to popcorn).

Also, in this case, the raw file can be anywhere in the disk, you don't need to worry with folder
structure. It can be inside the folder `popcorn/` if you'd like.

But guess what, we don't need to worry to call every single raw or even to import our model inside
our game, because we have:

***********
Data Core
***********
:class:`~panda_core_data.DataCore` is the class we use to access all the types, instances and data.
It's use is (hopefully) simple. Let's edit the file `/tutorial/main.py` to this:

.. code:: python

    from os.path import join, dirname, abspath
    from dataclasses import fields
    from panda_core_data import data_core

    def main():
        # Let's automatically get the folder named Popco- mods, I mean.
        mods_folder = join(dirname(abspath(__file__)), "mods")

        # Templates are something we will cover in the future, but for now
        # let's set them to False
        data_core(mods_folder, templates_folder=False)

        # If we use a for with a model class, we will get all instances of it.
        for instance in data_core.get_model_type("items"):
            print(f"\nValues for: {instance.name}")
            # Remember that I said our class turned into a dataclass?
            # We can iter along the fields now.
            for field in fields(instance):
                 print(f"\t{field.name}: {getattr(instance, field.name)}")


    if __name__ == '__main__':
        main()

This will output the values of our raw file without calling it, without even importing our model
and etc etc etc. So much if you like you can create another file in
`/tutorial/mods/core/raws/models/items/` and the instance will automatically be created.
