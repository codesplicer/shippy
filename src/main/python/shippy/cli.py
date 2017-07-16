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
shippy.cli
==========

Command-line entrypoint
"""
import logging
import argh
from shippy.repository_archive import RepositoryArchive
from shippy.data_volume import DataVolume
from shippy.config_loader import ConfigLoader
from shippy.container_stack import ContainerStack
from shippy import utils

LOGGER = logging.getLogger(__name__)


@argh.arg("configpath", type=str, help="Path to build config")
@argh.arg("appconfig", help="Path to application config")
@argh.arg("sha", type=str, help="Commit hash to build source from")
def deploy_stack(**kwargs):
    """
    Deploys an application stack
    """
    if not kwargs["sha"]:
        # raise KeyError("Missing --sha")
        LOGGER.error("You must specify a SHA with the --sha flag")
    sha = kwargs["sha"]

    if not kwargs["configpath"]:
        # raise KeyError("Missing --configpath")
        LOGGER.error("Missing --configpath")
    configpath = kwargs["configpath"]

    # 1. load and parse build configuration file
    LOGGER.info("Loading config...")
    config_loader = ConfigLoader(config_filepath=configpath, sha=sha)
    config = config_loader.get()

    # Create work directory
    workdir = "/tmp/shippy/archives/{app_name}_{sha}".format(app_name=config["app_name"], sha=sha)
    utils.create_directory(workdir)

    # 2. Fetch application sourcecode archive
    LOGGER.info("About to fetch repo archive...")
    repo = RepositoryArchive(config["application_repository"])
    download_path = repo.fetch(kwargs["sha"], download_path=workdir)
    LOGGER.info("Downloaded archive to: %s", download_path)

    # 3. Unpack sourcecode archive
    LOGGER.info("Downloaded archive to: %s", download_path)
    LOGGER.info("Unpacking archive")
    output_dir = utils.unpack_archive(download_path, config["app_name"], working_dir=workdir)
    LOGGER.info("Unpacked archive into: %s", output_dir)

    # 4. Run build commands
    for cmd in config["application_build_cmds"]:
        utils.execute_command(cmd, working_dir=output_dir)

    # 5. Copy application config file into sourcecode path root
    LOGGER.info("Copying application config file into: %s", output_dir)
    utils.copy_file(kwargs["appconfig"], output_dir)

    # 6. Build docker sourcecode data volume
    volume = DataVolume(output_dir, sha, config)
    volume.build()

    # 7. Build and write docker-compose stack configuration
    stack = ContainerStack(config, sha, output_dir, volume.get_name())
    stack.write_compose_file()

    # 8. Start docker-compose stack
    LOGGER.info("Starting container stack")
    stack.start()
    LOGGER.info("Stack is ready, have a nice day!")


@argh.arg("--sha", help="Commit hash to search for. If unspecified will return all running stacks", default="b37411239f70f538e198e238610a0e7e9c6b83b0")
def list_stacks(**kwargs):
    """
    Lists all running docker-compose stacks

    :param kwargs:
    :return:
    """
    # 1. get list of all running containers with the shippy prefix

    # 2. Build a prettytable chart

    # 3. Display table


@argh.arg("--sha", help="Commit hash to terminate stack for", default=None)
def terminate_stack(**kwargs):
    if not kwargs["sha"]:
        LOGGER.error("You must specify a stack to terminate with the --sha flag")
