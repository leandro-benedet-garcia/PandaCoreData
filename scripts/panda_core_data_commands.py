#!/usr/bin/env python
# encoding: utf-8
'''
:author: Leandro (Cerberus1746) Benedet Garcia
:license: MIT License
:contact: cerberus1746@gmail.com
'''

import sys
from os import makedirs
from os.path import join

from argparse import ArgumentParser
from panda_core_data import __version__

__version__ = __version__
__date__ = '2019-07-26'
__updated__ = '2019-07-26'

MAIN_FILE = """from os.path import join, dirname, abspath
from panda_core_data import data_core

def main():
    mods_folder = join(dirname(abspath(__file__)), "mods")
    data_core(mods_folder)

if __name__ == '__main__':
    main()
"""

BASE_MODEL = """from panda_core_data.model import Model

class ModelName(Model, data_name="model_name"):
    name: str
"""

#===================================================================================================
# BASE_TEMPLATE = """from panda_core_data.template import Template
#
# class TemplateName(Template, data_name="template_name"):
#     name: str
# """
#===================================================================================================

BASE_YAML_RAW = """data:
    - name: "name"
"""

BASE_JSON_RAW = """{"data": [
    {"name": "name"}
]}
"""

def create_file(path, contents):
    with open(path, 'w') as ofh:
        ofh.write(contents)

def main(argv=None):
    program_license = "Copyright 2019 Leandro (Cerberus1746) Benedet Garcia \
                      licensed under the MIT License"

    if argv is None:
        argv = sys.argv[1:]
    # setup option parser
    parser = ArgumentParser(description=program_license)
    parser.add_argument("-o", "--output", dest="outdir",
                        help="set output path [default: %default]", metavar="FILE")
    parser.add_argument("-re", "--raw_extension", dest="raw_extension",
                        help="set raw extension. The available extensions are yaml and json "
                        "[default: %default]")

    # set defaults
    parser.set_defaults(outfile=".", raw_extension="json")

    # process options
    opts = parser.parse_args(argv)

    if opts.outdir:
        if opts.raw_extension == "yaml":
            base_raw = BASE_JSON_RAW
        elif opts.raw_extension == "json":
            base_raw = BASE_JSON_RAW
        else:
            print(f"The extension {opts.raw_extension} is not supported, the options are yaml and "
                  "json")
            sys.exit()

        root = opts.outdir

        models_folder = join(root, "mods", "core", "models")
        # templates_folder = join(root, "mods", "core", "templates")

        raw_models = join(root, "mods", "core", "raws", "models")
        inner_raw_model = join(root, "mods", "core", "raws", "models", "model_name")
        # raw_templates = join(root, "mods", "core", "raws", "templates")

        makedirs(models_folder, exist_ok=True)
        # makedirs(templates_folder, exist_ok=True)

        makedirs(raw_models, exist_ok=True)
        makedirs(inner_raw_model, exist_ok=True)

        # makedirs(raw_templates, exist_ok=True)

        create_file(join(root, "main.py"), MAIN_FILE)
        create_file(join(models_folder, "example_model.py"), BASE_MODEL)
        # create_file(join(templates_folder, "example_template.py"), BASE_TEMPLATE)

        create_file(join(inner_raw_model, f"example_model_raw.{opts.raw_extension}"), base_raw)
        # create_file(join(raw_templates, "example_template_raw.yaml"), BASE_RAW)


if __name__ == "__main__":
    sys.exit(main())
