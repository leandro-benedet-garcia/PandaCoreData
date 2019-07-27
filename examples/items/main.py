'''
:created: 2019-07-25

:author: Leandro (Cerberus1746) Benedet Garcia
'''
from os.path import join, dirname, abspath
from dataclasses import fields
from panda_core_data import data_core

def main():
    return_value = []
    mods_folder = join(dirname(abspath(__file__)), "mods")
    data_core(mods_folder)
    for instance in data_core.get_model_type("items").all_instances():
        field_dict = {}
        for field in fields(instance):
            field_dict[field.name] = getattr(instance, field.name)

        return_value.append(field_dict)

    return return_value

if __name__ == '__main__':
    print(main())
