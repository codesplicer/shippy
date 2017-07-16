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
shippy.repository_archive
=========================

Parses and downloads archive file for a given github repository
"""
import os
import requests
import logging

from tqdm import tqdm
from utils import get_repository_username, get_repository_appname


GITHUB_API_BASEURL = "https://api.github.com"
LOGGER = logging.getLogger(__name__)


class RepositoryArchive:

    def __init__(self, url):
        self.url = url
        self.username = get_repository_username(url)
        self.repo_name = get_repository_appname(url)

    def get_archive_url(self, sha, format="tarball"):
        """
        Generates download URL for the given hash and format

        :param sha: (str) Commit hash to download
        :param format: Archive format [tarball, zipball]. Default: tarball
        :return: (str) Archive download URL
        """
        supported_formats = ["tarball", "zipball"]
        if format not in supported_formats:
            raise ValueError("The supplied format must be one of 'tarball' or 'zipball'")

        url_pattern = "{api_base}/repos/{user}/{reponame}/{format}/{ref}"
        archive_url = url_pattern.format(api_base=GITHUB_API_BASEURL, user=self.username, reponame=self.repo_name, format=format, ref=sha)
        return archive_url

    def fetch(self, sha, download_path="/tmp"):
        """
        Downloads the archive for the given commit hash

        :param sha: (str) Commit hash to download
        :param download_path: (str) Filesystem path to download archive to. Default: /tmp
        :return: (str) Full path to the downloaded archive
        """
        filename = "{0}.tar.gz".format(self.repo_name)
        local_filename = os.path.join(download_path, filename)
        download_url = self.get_archive_url(sha)

        LOGGER.info("Downloading to: %s", local_filename)
        r = requests.get(download_url, stream=True)

        # Get the total size in bytes
        total_size = int(r.headers.get("content-length", 0))

        with open(local_filename, 'wb') as f:
            for chunk in tqdm(r.iter_content(32 * 1024), total=total_size, unit="B", unit_scale=True):
                if chunk:
                    f.write(chunk)
        return local_filename
