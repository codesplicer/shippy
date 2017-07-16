import unittest
from shippy.config_loader import ConfigLoader

class TestConfig(unittest.TestCase):

    def setUp(self):
        self.mock_config = {
            "application_image": "tryghost/ghost",
            "application_repository": "https://github.com/tryghost/ghost",
            "application_source_mountpoint": "/usr/src/ghost",
            "application_config_filepath": "/full/path/to/configfile",
            "application_config": {
                "GHOST_URL": "http://www.example.com",
                "NODE_ENV": "production",
                "GHOST_SOURCE": "/usr/src/ghost",
                "DB_CLIENT": "mysql",
                "DB_USER": "ghost_user",
                "DB_PASSWORD": "ghostadmin1234",
                "DB_HOST": "db"
            },
            "database_image": "mysql/mysql-server",
            "database_config": {
                "MYSQL_USER": "ghost_user",
                "MYSQL_PASSWORD": "ghostadmin1234",
                "MYSQL_DATABASE": "ghost"
            }
        }

    # def test_validate_config(self):
    #     config = ConfigLoader()
    #     assert config.validate_config(self.mock_config) == self.mock_config
    #
    # def test_invalid_config(self):
    #     invalid_config = {
    #         "app_image": "tryghost/ghost"
    #     }
    #     with self.assertRaises(ValueError):
    #         config.validate_config(invalid_config)