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
shippy.config
==============

Parses and validates the build config file

"""
import json
import validictory
import logging

from collections import ChainMap
from shippy.utils import get_repository_appname

LOGGER = logging.getLogger(__name__)


class ConfigLoader:

    def __init__(self, config_filepath, sha):
        self.config_filepath = config_filepath
        self.sha = sha
        self.config = self._open()

    def _load(self):
        """
        Loads and parses config file

        :param config_filepath: (str) Filepath to config file
        :return: (dict) Parsed config
        """
        with open(self.config_filepath) as config_file:
            config = json.load(config_file)
        return config

    def _compute_config(self, config):
        """
        Generates additional config to append to main config object
        based on computed values

        :return: (dict)
        """
        extra_config = {
            "app_name": get_repository_appname(config["application_repository"]),
            "app_sha": self.sha
        }

        return extra_config

    def _open(self):
        """
        Returns complete config object

        :return: (dict) Config object
        """
        # Read and validate config
        original_config = self._load()
        self.validate(original_config)

        # Generate additional computed config
        extra_config = self._compute_config(original_config)

        # Stitch the dictionaries together
        config = dict(ChainMap(extra_config, original_config))

        return config

    def get(self):
        """
        Returns the config

        :return: (dict)
        """
        return self.config

    @staticmethod
    def validate(config):
        """
        Validates config conforms with expected schema

        :param config:
        :return: (dict) Validated config
        :raises: (ValueError) when invalid config is found
        """
        schema = {
            "type": "object",
            "properties": {
                "application_image": {
                    "type": "string",
                    "required": True
                },
                "application_repository": {
                    "type": "string",
                    "required": True
                },
                "application_source_mountpoint": {
                    "type": "string",
                    "required": True
                },
                "application_config": {
                    "type": "object",
                    "required": True,
                },
                "database_image": {
                    "type": "string",
                    "required": True
                },
                "database_config": {
                    "type": "object",
                    "required": True
                }
            }
        }

        try:
            validictory.validate(config, schema)
        except ValueError as e:
            LOGGER.error("Invalid config: %s", e)
            raise e

        return config
