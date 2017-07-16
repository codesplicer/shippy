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


def _get_repo_path(repo_url):
    """
    Extracts the username/reponame from the given github URL

    :param repo_url: (str) Full https path to the github repository
    :return: (str) <username>/<reponame>
    """
    position = repo_url.find("github.com")
    name = ""
    if position >= 0:
        name = repo_url[position + 11:]
        if name.endswith("/"):
            # Strip trailing slash
            name = name[:-1]
    else:
        if repo_url.endswith("/"):
            name = repo_url[:-1]
    return name.split("/")


def get_repository_username(repo_url):
    """
    Returns the repository username

    :return: (str) Repository owner username
    """
    repo_path = _get_repo_path(repo_url)
    return repo_path[0]


def get_repository_appname(repo_url):
    """
    Returns the repository name

    :return: (str) Repository name
    """
    repo_path = _get_repo_path(repo_url)
    return repo_path[1]

def unpack_archive(archive_path, app_name, working_dir=None):
    """
    Unpacks the github tarball at the specified path.

    The tarball has a top-level directory named after the project and hash, so when unpacking this
    gets removed

    :param archive_path:
    :param app_name:
    :param working_dir:
    :return:
    """
    # /tmp/ghost-sha
    LOGGER.info("About to unpack archive: %s", archive_path)
    cmd = "mkdir -p {working_dir}/{app_name} && tar xvfz {archive_path} -C {working_dir}/{app_name} --strip-components 1".format(app_name=app_name, archive_path=archive_path, working_dir=working_dir)

    LOGGER.info("Running command: %s", cmd)
    try:
        check_call(cmd, shell=True)
    except CalledProcessError as e:
        LOGGER.error(e)
        raise SystemExit(1)

    output_dir = "{working_dir}/{app_name}".format(working_dir=working_dir, app_name=app_name)
    return output_dir


def create_directory(dir):
    """
    Creates the specified directory if it doesn't exist, including all
    intermediate directories.

    :param dir: (str) Directory path to create
    :return:
    """
    try:
        os.makedirs(dir)
    except OSError as e:
        # Ignore if it already exists
        if e.errno != errno.EEXIST:
            # We have some other disk error
            raise

