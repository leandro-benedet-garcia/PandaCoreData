#!/usr/bin/env python
# encoding: utf-8
'''
:author:     Leandro (Cerberus1746) Benedet Garcia
:license:    MIT License
:contact:    cerberus1746@gmail.com
'''

import sys
from os import makedirs
from os.path import join

from argparse import ArgumentParser
from panda_core_data import __version__

__version__ = __version__
__date__ = '2019-07-26'
__updated__ = '2019-07-26'

BASE_MODEL = """from panda_core_data.model import Model

class ModelName(Model, data_name="model_name"):
    name: str
"""

BASE_TEMPLATE = """from panda_core_data.template import Template

class TemplateName(Template, data_name="template_name"):
    name: str
"""

BASE_RAW = """data:
    - name: "name"
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
    parser.add_argument("-o", "--out", dest="outdir",
                        help="set output path [default: %default]", metavar="FILE")

    # set defaults
    parser.set_defaults(outfile=".")

    # process options
    (opts, _) = parser.parse_args(argv)

    if opts.outdir:
        root = opts.outdir

        models_folder = join(root, "mods", "core", "models")
        templates_folder = join(root, "mods", "core", "templates")

        raw_models = join(root, "mods", "core", "raws", "models")
        inner_raw_model = join(root, "mods", "core", "raws", "models", "model_name")
        raw_templates = join(root, "mods", "core", "raws", "templates")

        makedirs(models_folder, exist_ok=True)
        makedirs(templates_folder, exist_ok=True)

        makedirs(raw_models, exist_ok=True)
        makedirs(inner_raw_model, exist_ok=True)
        makedirs(raw_templates, exist_ok=True)

        create_file(join(models_folder, "example_model.py"), BASE_MODEL)
        create_file(join(templates_folder, "example_template.py"), BASE_TEMPLATE)
        create_file(join(inner_raw_model, "model_name.yaml"), BASE_RAW)
        create_file(join(raw_templates, "template_name.yaml"), BASE_RAW)


if __name__ == "__main__":
    sys.exit(main())
