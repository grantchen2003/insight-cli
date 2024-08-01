from unittest.mock import patch, MagicMock
import unittest

from insight_cli.api import QueryRepositoryAPI
from insight_cli.config import config


class TestQueryRepositoryAPI(unittest.TestCase):
    @patch("requests.get")
    def test_make_request(self, mock_request_get):
        expected_response = []
        mock_request_get.return_value = MagicMock(
            json=lambda: expected_response,
            raise_for_status=lambda: None,
        )

        repository_id = "test_repo_id"
        query_string = "water"
        limit = 1

        self.assertEqual(
            QueryRepositoryAPI().make_request(repository_id, query_string, limit),
            expected_response,
        )

        mock_request_get.assert_called_once_with(
            url=f"{config.INSIGHT_API_BASE_URL}/query_repository",
            json={
                "repository_id": repository_id,
                "query_string": query_string,
                "limit": limit,
            },
        )


if __name__ == "__main__":
    unittest.main()
