import unittest
from configparser import ConfigParser

from pyllegro import AllegroWebApi

API_KEY = 'test'
USERNAME = 'test'
PASSWORD = 'test'


class TestingAllegroWebApi(unittest.TestCase):
    def test_default_sandbox_environment(self):
        a = AllegroWebApi(API_KEY)
        self.assertTrue(a.sandbox)
        self.assertTrue('sandbox' in a.client.wsdl.url)


if __name__ == '__main__':
    # todo: change config reading
    config = ConfigParser()
    config.read('local.ini')  # test_config.ini file here
    API_KEY = config.get('allegro', 'api-key')
    USERNAME = config.get('allegro', 'username')
    PASSWORD = config.get('allegro', 'password')
    unittest.main()
