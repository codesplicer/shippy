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
from docker import AutoVersionClient

LOGGER = logging.getLogger(__name__)
DOCKERFILE_TEMPLATE = '''
FROM busybox

# Create source directory
RUN mkdir -p {{ target_sourcepath }}
RUN chmod -R 777 {{ target_sourcepath }}

ADD {{ source_archivedir }} {{ target_sourcepath }}

VOLUME {{ target_sourcepath }}

LABEL version={{ source_sha }}
LABEL maintainer="Vik Bhatti (github@vikbhatti.com)"

'''


class DataVolume:

    def __init__(self, sourcecode_path, sha, config):
        """
        Constructor

        :param sourcecode_path:
        :param sha:
        :param config:
        """
        self.sourcecode_path = sourcecode_path
        self.sha = sha
        self.config = config
        self.cli = AutoVersionClient(base_url='unix://var/run/docker.sock')
        self.volume_name = self._generate_name()

    def _generate_name(self):
        """
        Generates a name for the data volume

        :return:
        """
        volume_name = "{app_name}_data_{sha}".format(app_name=self.config["app_name"], sha=self.sha)
        return volume_name

    def build(self):
        """
        Builds a docker data volume

        """
        '''
        1. copy sourcecode path into volume
        2. create named docker volume.
            In order to facilitate lookup for cleanup, we need to
            be able to search based on standard naming convention (or image label)
        '''
        f = BytesIO(DOCKERFILE_TEMPLATE.encode("utf-8"))

        LOGGER.info("Creating docker data volume")
        response = [line for line in self.cli.build(fileobj=f, rm=True, tag=self.volume_name)]
        LOGGER.info(response)

    def remove(self):
        """
        Deletes an image

        :return:
        """
        LOGGER.info("Removing image: %s", self.volume_name)
        response = [line for line in self.cli.remove(image=self.volume_name, force=True)]
        LOGGER.info(response)
