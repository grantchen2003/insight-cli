from unittest.mock import patch, MagicMock
import unittest

from insight_cli.api import CreateRepositoryAPI
from insight_cli.config import config


class TestCreateRepositoryAPI(unittest.TestCase):
    @patch("requests.post")
    def test_make_request(self, mock_request_post):
        expected_response = {"repository_id": "mock_repository_id"}
        
        mock_request_post.return_value = MagicMock(
            json=lambda: expected_response,
            raise_for_status=lambda: None,
        )
        
        self.assertEqual(
            CreateRepositoryAPI().make_request(),
            expected_response,
        )

        mock_request_post.assert_called_once_with(
            url=f"{config.INSIGHT_API_BASE_URL}/create_repository"
        )


if __name__ == "__main__":
    unittest.main()
