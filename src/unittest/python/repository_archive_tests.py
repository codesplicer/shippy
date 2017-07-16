import unittest
from shippy.repository_archive import RepositoryArchive


class TestRepositoryArchive(unittest.TestCase):

    def setUp(self):
        self.repo_url = "https://github.com/codesplicer/shippy"
        self.repo = RepositoryArchive(self.repo_url)
        self.sha = "1234abcd"

    def test_get_username(self):
        # repo = repository.Repository(self.repo_url)
        assert self.repo._get_username() == "codesplicer"

    def test_get_reponame(self):
        repo = RepositoryArchive(self.repo_url)
        assert self.repo._get_reponame() == "shippy"

    def test_get_archive_url(self):
        assert self.repo.get_archive_url(self.sha) == "https://api.github.com/repos/codesplicer/shippy/tarball/1234abcd"

    def test_fetch(self):
        # Need to mock requests, test that it hits the right URL
        # Or mock object and assert that it was called?
        # Send a mock object that returns a generator?
        # Would also need to mock out file.write
        pass
