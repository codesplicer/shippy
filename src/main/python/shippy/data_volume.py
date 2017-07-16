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
shippy.data_volume
===================

Builds and manages a docker data volume with the provided sourcecode

"""
import logging
from io import BytesIO
import docker
from copy import deepcopy

LOGGER = logging.getLogger(__name__)
DOCKERFILE_TEMPLATE = """\
FROM busybox

# Create source directory
RUN groupadd -r user && useradd -r -g user user
RUN mkdir -p {mountpoint} && chown -R user:user {mountpoint}
RUN chmod -R 777 {mountpoint}
ADD . {mountpoint}
VOLUME {mountpoint}
LABEL version={source_sha}
LABEL maintainer="Vik Bhatti (github@vikbhatti.com)"

"""


class DataVolume:

    def __init__(self, sourcecode_path, sha, config):
        """
        Constructor

        :param sourcecode_path: (str) Path to unpacked sourcecode for the given hash
        :param sha: (str) Commit hash to work on
        :param config: (dict) Configuration object as parsed by shippy.config
        """
        self.sourcecode_path = sourcecode_path
        self.sha = sha
        self.config = deepcopy(config)
        self.cli = APIClient(base_url='unix://var/run/docker.sock')
        self.volume_name = self._generate_name()

    def _generate_name(self):
        """
        Generates a name for the data volume

        :return: (str) Volume name
        """
        volume_name = "{app_name}_data_{sha}".format(app_name=self.config["app_name"], sha=self.sha)
        return volume_name

    def get_name(self):
        """
        Returns name of the docker volume

        :return:(str) Name of the docker volume tag
        """
        return self.volume_name

    def _render_template(self):
        """
        Renders dockerfile template

        :return: (str) Rendered template
        """
        data = {
            "mountpoint": self.config["application_source_mountpoint"],
            "source_archivedir": self.sourcecode_path,
            "source_sha": self.sha
        }

        template = DOCKERFILE_TEMPLATE.format(**data)
        return template

    def _write_dockerfile(self):
        """
        Writes a dockerfile into the source path

        :return: None
        """
        template = self._render_template()
        dockerfile_path = "{sourcepath}/Dockerfile".format(sourcepath=self.sourcecode_path)
        LOGGER.info("Writing dockerfile to: %s", dockerfile_path)
        with open(dockerfile_path, "w") as f:
            try:
                f.write(template)
            except OSError as e:
                LOGGER.error("Could not write dockerfile")
                LOGGER.error(e)
                raise SystemExit(1)

    def build(self):
        """
        Builds a docker data volume

        :return: None
        """
        '''
        1. copy sourcecode path into volume
        2. create named docker volume.
            In order to facilitate lookup for cleanup, we need to
            be able to search based on standard naming convention (or image label)
        '''
        # Write dockerfile
        self._write_dockerfile()
        LOGGER.info("Creating docker data volume")

        try:
            response = self.cli.build(path=self.sourcecode_path, rm=True, tag=self.volume_name)
        except docker.errors.BuildError as e:
            LOGGER.error("Problem building docker image")
            LOGGER.error(e)
            raise SystemExit(1)

        for line in response:
            LOGGER.info(line)

    def remove(self):
        """
        Deletes the docker image

        :return: None
        """
        LOGGER.info("Removing image: %s", self.volume_name)
        response = [line for line in self.cli.remove(image=self.volume_name, force=True)]
        LOGGER.info(response)
