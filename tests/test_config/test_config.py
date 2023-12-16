import unittest

from insight_cli.config import config


class TestConfig(unittest.TestCase):
    def test_version(self):
        expected_version = "0.0.0"
        self.assertEqual(config.INSIGHT_VERSION, expected_version)

    def test_api_base_url(self):
        expected_base_url = "http://127.0.0.1:5000"
        self.assertEqual(config.INSIGHT_API_BASE_URL, expected_base_url)


if __name__ == "__main__":
    unittest.main()
