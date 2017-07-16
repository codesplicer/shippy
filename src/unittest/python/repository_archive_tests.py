import unittest
from shippy.repository_archive import RepositoryArchive


class TestRepositoryArchive(unittest.TestCase):

    def setUp(self):
        self.repo_url = "https://github.com/codesplicer/shippy"
        self.repo = RepositoryArchive(self.repo_url)
        self.sha = "1234abcd"

    def test_get_archive_url(self):
        assert self.repo.get_archive_url(self.sha) == "https://api.github.com/repos/codesplicer/shippy/tarball/1234abcd"

    def test_fetch(self):
        # Need to mock requests, test that it hits the right URL
        pass
