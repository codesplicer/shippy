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
shippy.container_stack
=======================

Builds docker-compose configurations for the stacks, and handles setup and teardown of container resources
"""
# import json
import logging
# import os
from shippy import utils
from copy import deepcopy

# from shippy.utils import get_template_filepath
from shippy.utils import load_template, get_repository_appname, run_command

LOGGER = logging.getLogger(__name__)


class ContainerStack:

    def __init__(self, config, sha, working_dir, volume_tag):
        self.config = deepcopy(config)
        self.sha = sha
        self.working_dir = working_dir
        # self.volume_name = volume_name
        self.volume_tag = volume_tag
        self.compose_filepath = None

    def _generate_name(self):
        """
        Generates a stack name based on the application name and sha

        :return: (str) Stack name
        """
        repo_name = get_repository_appname(self.config["application_repository"])
        stack_name = "{repo_name}_{sha}".format(repo_name=repo_name, sha=self.sha)
        return stack_name

    def _assemble_template_data(self):
        """
        Assembles data for use by the jinja config template

        :return: (dict) Template config
        """
        data = {
            "data_volume_tag": self.volume_tag,
            "source_image_tag": self.config["application_image"],
            "db_image_tag": self.config["database_image"],
            "database_config": self.config["database_config"],
            "application_name": get_repository_appname(self.config["application_repository"]),
            "app_image_tag": self.config["application_image"],
            "application_config": self.config["application_config"],
            "sha": self.sha
        }
        return data

    def _build_template(self, template_data, template_name="docker-compose.yml.j2"):
        """
        Takes the required config for the stack and converts it into a format ready for the jinja2 template to render

        :param template_data: (dict) Template data to use for rendering the config
        :return: (jinja2 template)
        """
        return load_template(template_name).render(template_data)

    def write_compose_file(self, destination=None):
        """
        Writes the generated docker-compose config to working_dir, or alternate
        destination if specified

         NB - The compose file will be prefixed by the short hash and component name
         This way

         :param destination: (str) Alternate path to write docker-compose file to. Default: None
        :return:
        """
        if destination:
            dest = destination
        else:
            dest = self.working_dir

        template_data = self._assemble_template_data()
        template = self._build_template(template_data)

        # Need to write the template to the correct path
        target = "{destination_dir}/docker-compose.yml".format(destination_dir=dest)
        LOGGER.info("Writing docker-compose file to: %s", target)

        with open(target, "w") as f:
            f.write(template)
            self.compose_filepath = target

    def start(self):
        """
        Starts the stack using docker-compose

        :return:
        """
        context = "{app_name}_{sha}".format(app_name=self.config["app_name"], sha=self.sha)
        # cmd = "/usr/local/bin/docker-compose -p {context} --project-directory {project_dir} up -d".format(context=context, project_dir=self.working_dir)
        # cmd = "/usr/local/bin/docker-compose -p {context} -f {compose_file} up -d".format(context=context, compose_file=self.compose_filepath)
        cmd = "/usr/local/bin/docker-compose -p {context} up -d".format(context=context)
        # execute_command(cmd, working_dir=self.working_dir)
        utils.execute_command(cmd, working_dir=self.working_dir)

    def stop(self):
        """
        Stops the stack using docker-compose

        :return:
        """
        context = "{app_name}_{sha}".format(app_name=self.config["app_name"], sha=self.sha)
        cmd = "/usr/local/bin/docker-compose -p {context} --project-directory {project_dir} stop".format(context=context, project_dir=self.working_dir)
        run_command(cmd)

    def terminate(self):
        """
        Terminates all containers associated with the stack using docker-compose

        :return:
        """
        context = "{app_name}_{sha}".format(app_name=self.config["app_name"], sha=self.sha)
        cmd = "/usr/local/bin/docker-compose -p {context} --project-directory {project_dir} down --rmi all".format(context=context, project_dir=self.working_dir)
        run_command(cmd)

    def list(self):
        """
        Lists the components of the stack, along with their state

        :return:
        """
