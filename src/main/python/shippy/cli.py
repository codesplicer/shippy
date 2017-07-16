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
from shippy.data_volume import DataVolume
from shippy.config_loader import ConfigLoader
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

