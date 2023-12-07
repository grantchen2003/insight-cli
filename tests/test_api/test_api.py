from unittest.mock import Mock, patch
import json
import unittest

from insight_cli.api import API
from insight_cli.config import config
from insight_cli.utils import Directory
from insight_cli.utils.file import File


class TestAPI(unittest.TestCase):
    @patch("requests.post")
    def test_make_initialize_repository_request_with_empty_repository_directory(
        self, mock_request_post
    ) -> None:
        mock_response = Mock()
        mock_response.json.return_value = {"repository_id": "12312"}
        mock_request_post.return_value = mock_response

        repository_dir = Directory("empty_directory")

        response = API.make_initialize_repository_request(repository_dir)

        mock_request_post.assert_called_with(
            url=f"{config.INSIGHT_API_BASE_URL}/initialize_repository",
            json=json.dumps(
                {
                    "repository_dir": repository_dir.to_dict(),
                },
                default=str,
            ),
        )
        self.assertTrue("repository_id" in response)
        self.assertIsInstance(response["repository_id"], str)

    @patch("requests.post")
    def test_make_initialize_repository_request_with_non_empty_directory(
        self, mock_request_post
    ) -> None:
        mock_response = Mock()
        mock_response.json.return_value = {"repository_id": "12312"}
        mock_request_post.return_value = mock_response

        subdirectory = Directory("non_empty_subdirectory")
        subdirectory.add_file(File("empty_file", []))
        repository_dir = Directory("non_empty_directory")
        repository_dir.add_file(File("empty_file", []))
        repository_dir.add_subdirectory(subdirectory)

        response = API.make_initialize_repository_request(repository_dir)

        mock_request_post.assert_called_with(
            url=f"{config.INSIGHT_API_BASE_URL}/initialize_repository",
            json=json.dumps(
                {
                    "repository_dir": repository_dir.to_dict(),
                },
                default=str,
            ),
        )
        self.assertTrue("repository_id" in response)
        self.assertIsInstance(response["repository_id"], str)

    @patch("requests.post")
    def test_make_reinitialize_repository_request_with_valid_repository(
        self, mock_request_post
    ) -> None:
        mock_request_post.return_value = Mock()

        subdirectory = Directory("non_empty_subdirectory")
        subdirectory.add_file(File("empty_file", []))
        repository_dir = Directory("non_empty_directory")
        repository_dir.add_file(File("empty_file", []))
        repository_dir.add_subdirectory(subdirectory)
        repository_id = "123"

        API.make_reinitialize_repository_request(repository_dir, repository_id)

        mock_request_post.assert_called_with(
            url=f"{config.INSIGHT_API_BASE_URL}/reinitialize_repository",
            json=json.dumps(
                {
                    "repository_dir": repository_dir.to_dict(),
                    "repository_id": repository_id,
                },
                default=str,
            ),
        )

    @patch("requests.post")
    def test_make_validate_repository_id_request_with_valid_repository_id(
        self, mock_request_post
    ) -> None:
        repository_id_is_valid = True
        mock_response = Mock()
        mock_response.json.return_value = {
            "repository_id_is_valid": repository_id_is_valid
        }
        mock_request_post.return_value = mock_response

        repository_id = "123"

        response = API.make_validate_repository_id_request(repository_id)

        mock_request_post.assert_called_with(
            url=f"{config.INSIGHT_API_BASE_URL}/validate_repository_id",
            json=json.dumps(
                {"repository_id": repository_id},
                default=str,
            ),
        )
        self.assertEqual(response["repository_id_is_valid"], repository_id_is_valid)

    @patch("requests.post")
    def test_make_validate_repository_id_request_with_invalid_repository_id(
        self, mock_request_post
    ) -> None:
        repository_id_is_valid = False
        mock_response = Mock()
        mock_response.json.return_value = {
            "repository_id_is_valid": repository_id_is_valid
        }
        mock_request_post.return_value = mock_response

        repository_id = "123"

        response = API.make_validate_repository_id_request(repository_id)

        mock_request_post.assert_called_with(
            url=f"{config.INSIGHT_API_BASE_URL}/validate_repository_id",
            json=json.dumps(
                {"repository_id": repository_id},
                default=str,
            ),
        )
        self.assertEqual(response["repository_id_is_valid"], repository_id_is_valid)


if __name__ == "__main__":
    unittest.main()
