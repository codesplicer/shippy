#  shippy
#  Copyright 2017 Vik Bhatti
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""
shippy.utils
============

Various utility functions
"""
import os
import shutil
import errno
import logging
import asyncio
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from subprocess import CalledProcessError, check_call

LOGGER = logging.getLogger(__name__)


def get_template_filepath(filename, basepath="templates"):
    """
    Get the full path to the config templates, using a relative path to where the shippy script is stored

    :param filename: (str) Name of the template file to look for
    :param basepath: (str) Base directory to search for templates. Default: /templates
    :return: (str) Path to template if found
    :raises: (SystemExit) If template file doesn't exist
    """
    local_path = os.path.dirname(__file__)
    print("===================")
    print(local_path)
    print("===================")
    path = os.path.dirname(os.path.abspath(os.path.join(local_path, basepath, filename)))

    if os.path.isdir(path):
        return path
    else:
        raise SystemExit(f"Could not find template files in: {path}, bailing...")


def load_template(name):
    """
    Loads the given jinja template file

    :param name: (str) Name of the template file
    :return: (object) Instance of jinja2 template
    """
    template_path = get_template_filepath(name)
    template_loader = FileSystemLoader(template_path)
    template_env = Environment(loader=template_loader, autoescape=False, extensions=["jinja2.ext.autoescape"])

    try:
        template = template_env.get_template(name)
    except TemplateNotFound as e:
        raise SystemExit("Could not find jinja template: %s", e)

    return template
