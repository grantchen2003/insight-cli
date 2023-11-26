from datetime import datetime
from unittest.mock import Mock, patch
import json
import unittest

from insight_cli.core.api import (
    make_initialize_repository_request,
    make_reinitialize_repository_request,
    make_validate_repository_id_request,
    get_base_api_url,
)
from insight_cli.utils.directory import Directory
from insight_cli.utils.file import File


class TestApi(unittest.TestCase):
    @patch("requests.post")
    def test_make_initialize_repository_request_with_empty_directory(
        self, mock_request_post
    ) -> None:
        mock_response = Mock()
        mock_response.json.return_value = {"repository_id": "12312"}
        mock_request_post.return_value = mock_response

        repository_dir = Directory("dir_name", datetime.now())
        response = make_initialize_repository_request(repository_dir)

        self.assertTrue("repository_id" in response)
        self.assertIsInstance(response["repository_id"], str)

    @patch("requests.post")
    def test_make_initialize_repository_request_with_non_empty_directory(
        self, mock_request_post
    ) -> None:
        mock_response = Mock()
        mock_response.json.return_value = {"repository_id": "12312"}
        mock_request_post.return_value = mock_response

        file1 = File("fil1", datetime.now(), [])
        file2 = File("fil2", datetime.now(), [])
        subdirectory = Directory("subdir", datetime.now())
        subdirectory.add_file(file2)
        repository_dir = Directory("dir_name", datetime.now())
        repository_dir.add_file(file1)
        repository_dir.add_subdirectory(subdirectory)

        response = make_initialize_repository_request(repository_dir)

        self.assertTrue("repository_id" in response)
        self.assertIsInstance(response["repository_id"], str)
        mock_request_post.assert_called_with(
            url=f"{get_base_api_url()}/initialize_repository",
            json=json.dumps(
                {
                    "repository": repository_dir.to_dict(),
                },
                default=str,
            ),
        )

    @patch("requests.post")
    def test_make_reinitialize_repository_request(self, mock_request_post) -> None:
        mock_response = Mock()
        mock_response.json.return_value = {"repository_id": "12312"}
        mock_request_post.return_value = mock_response

        file1 = File("fil1", datetime.now(), [])
        file2 = File("fil2", datetime.now(), [])
        subdirectory = Directory("subdir", datetime.now())
        subdirectory.add_file(file2)
        repository_dir = Directory("dir_name", datetime.now())
        repository_dir.add_file(file1)
        repository_dir.add_subdirectory(subdirectory)
        repository_id = "123"

        make_reinitialize_repository_request(repository_dir, repository_id)
        mock_request_post.assert_called_with(
            url=f"{get_base_api_url()}/reinitialize_repository",
            json=json.dumps(
                {
                    "repository": repository_dir.to_dict(),
                    "repository_id": repository_id,
                },
                default=str,
            ),
        )

    @patch("requests.post")
    def test_make_reinitialize_repository_request(self, mock_request_post) -> None:
        repository_id_is_valid = True
        mock_response = Mock()
        mock_response.json.return_value = {
            "repository_id_is_valid": repository_id_is_valid
        }
        mock_request_post.return_value = mock_response

        repository_id = "123"
        response = make_validate_repository_id_request(repository_id)

        self.assertEqual(response["repository_id_is_valid"], repository_id_is_valid)


if __name__ == "__main__":
    unittest.main()
