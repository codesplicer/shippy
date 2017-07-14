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

MAINTAINER Vik Bhatti <github@vikbhatti.com>

# Create source directory
RUN mkdir -p {{ target_sourcepath }}
RUN chmod -R 777 {{ target_sourcepath }}

ADD {{ source_archivedir }} {{ target_sourcepath }}

VOLUME {{ target_sourcepath }}

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

