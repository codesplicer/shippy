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
A simple project that builds and deploys a docker container based on a repository SHA

"""

from pybuilder.core import use_plugin, init, Author

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.install_dependencies")
use_plugin("python.flake8")
use_plugin("python.coverage")
use_plugin("filter_resources")
use_plugin("python.distutils")

name = "shippy"
authors = [Author("Vik Bhatti", "github@vikbhatti.com")]
license = "Apache License, Version 2.0"
url = "https://github.com/codesplicer/shippy"
summary = "Application to build and deploy docker containers based on a repository commit hash"
version = "0.1.0"

default_task = ["clean", "install_dependencies", "analyze", "publish"]


@init
def set_properties(project):
    project.build_depends_on("coverage")
    project.depends_on_requirements("requirements.txt")
    # project.build_depends_on_requirements("requirements-dev.txt")

    project.set_property("name", "shippy")
    project.set_property("verbose", True)

    # Set coverage properties
    project.set_property("coverage_break_build", False)
    project.set_property("coverage_threshold_warn", 70)  # Fail the build if coverage drops below 70%

    # Set linter properties
    project.set_property("flake8_break_build", True)
    project.set_property("flake8_ignore", "E501")  # Ignore lines longer than 80 chars
    project.set_property("flake8_verbose_output", True)

    project.get_property('filter_resources_glob').append('**/shippy/__init__.py')
