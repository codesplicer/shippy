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

from logging import getLogger, Formatter, INFO, StreamHandler

__author__ = "Vik Bhatti"
__version__ = "${version}"


# LOGGING_FORMAT = "%(asctime)-15s: %(name)s: %(levelname)-8s : %(filename)s:%(lineno)s - %(funcName)20s() : %(message)s"
LOGGING_FORMAT = "%(asctime)-15s: %(name)s: %(levelname)-8s : %(message)s"


def initialise_root_logger(log_level=INFO):
    """
    Returns a root logger with logs to stdout using the given log_level
    """
    formatter = Formatter(LOGGING_FORMAT)

    console_handler = StreamHandler()
    console_handler.setFormatter(formatter)

    root_logger = getLogger(__name__)
    root_logger.setLevel(log_level)
    root_logger.addHandler(console_handler)
    return root_logger


# Setup the module-level logger
LOGGER = initialise_root_logger(INFO)
