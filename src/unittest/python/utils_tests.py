import unittest
import os
from shippy import utils
from unittest import mock

class TestUtils(unittest.TestCase):

    def setUp(self):
        self.repo_url = "https://github.com/codesplicer/shippy"

    def test_get_template_filepath_on_valid_file(self):
        filename = "docker-compose.yml.j2"
        expected_basepath = os.path.abspath("src/main/python/shippy/templates/")
        mocked_isdir = mock.MagicMock()
        with mock.patch("os.path.isdir",
                        mocked_isdir,
                        spec=True):
            mocked_isdir.return_value = True
            actual_path = utils.get_template_filepath(filename)
            assert expected_basepath == actual_path

    def test_get_template_filepath_on_invalid_file(self):
        filename = "foobar.j2"
        mocked_isdir = mock.MagicMock()
        with mock.patch("os.path.isdir",
                        mocked_isdir,
                        spec=True):
            mocked_isdir.return_value = False
            with self.assertRaises(SystemExit):
                utils.get_template_filepath(filename)

    def test_get_repo_path(self):
        expected_repo_path = ["codesplicer", "shippy"]
        actual_repo_path = utils._get_repo_path(self.repo_url)
        print(actual_repo_path)
        assert actual_repo_path == expected_repo_path

    def test_get_repository_username(self):
        assert utils.get_repository_username(self.repo_url) == "codesplicer"

    def test_get_repository_appname(self):
        assert utils.get_repository_appname(self.repo_url) == "shippy"
