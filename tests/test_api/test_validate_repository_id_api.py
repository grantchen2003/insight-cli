from unittest.mock import patch
import unittest

from insight_cli.api import ValidateRepositoryIdAPI
from insight_cli.config import config


class TestValidateRepositoryIdAPI(unittest.TestCase):
    @patch("requests.post")
    def test_make_request(self, mock_request_get):
        repository_id = "test_repo_id"

        ValidateRepositoryIdAPI().make_request(repository_id),

        mock_request_get.assert_called_once_with(
            url=f"{config.INSIGHT_API_BASE_URL}/validate_repository_id",
            json={"repository_id": repository_id},
        )


if __name__ == "__main__":
    unittest.main()
