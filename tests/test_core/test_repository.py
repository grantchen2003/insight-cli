from datetime import datetime
from pathlib import Path
from unittest.mock import Mock, patch
import json
import os
import shutil
import unittest

from insight_cli.core import api
from insight_cli.core import dot_insight_dir
from insight_cli.core.repository import initialize, reinitialize, uninitialize
from insight_cli.utils.directory import Directory


class TestRepository(unittest.TestCase):
    def setUp(self) -> None:
        self.test_temp_folder_path = Path("./tests/test_core/temp_test_repository")
        if not os.path.exists(self.test_temp_folder_path):
            os.makedirs(self.test_temp_folder_path)

    def tearDown(self):
        shutil.rmtree(self.test_temp_folder_path)

    @patch("insight_cli.core.dot_insight_dir.is_valid")
    @patch("requests.post")
    def test_initialize_with_existing_dot_insight_dir(
        self,
        mock_requests_post,
        mock_is_valid,
    ) -> None:
        repository_dir_path = self.test_temp_folder_path

        dot_insight_dir_path: Path = (
            repository_dir_path / dot_insight_dir.get_dir_name()
        )
        repository_id = "123"
        dot_insight_dir.create(dot_insight_dir_path, repository_id)

        mock_is_valid.return_value = True

        initialize(repository_dir_path)

        mock_requests_post.assert_called_with(
            url=f"{api.get_base_api_url()}/reinitialize_repository",
            json=json.dumps(
                {
                    "repository": Directory.create_from_path(
                        repository_dir_path
                    ).to_dict(),
                    "repository_id": repository_id,
                },
                default=str,
            ),
        )

    @patch("requests.post")
    def test_initialize_with_non_existing_dot_insight_dir(
        self,
        mock_requests_post,
    ) -> None:
        repository_dir_path = self.test_temp_folder_path

        mock_response = Mock()
        mock_response.json.return_value = {"repository_id": "123"}
        mock_requests_post.return_value = mock_response

        repository = Directory.create_from_path(repository_dir_path)

        initialize(repository_dir_path)

        mock_requests_post.assert_called_with(
            url=f"{api.get_base_api_url()}/initialize_repository",
            json=json.dumps(
                {"repository": repository.to_dict()},
                default=str,
            ),
        )

    def test_reinitialize_with_invalid_path(self) -> None:
        invalid_path: Path = self.test_temp_folder_path / "invalid_path"
        with self.assertRaises(dot_insight_dir.InvalidDotInsightDirectoryPathError):
            reinitialize(invalid_path)

    @patch("requests.post")
    def test_reinitialize_with_valid_path(self, mock_requests_post) -> None:
        repository_dir_path = self.test_temp_folder_path
        dot_insight_dir_path: Path = (
            repository_dir_path / dot_insight_dir.get_dir_name()
        )
        repository_id = "123"
        dot_insight_dir.create(dot_insight_dir_path, repository_id)

        repository = Directory.create_from_path(repository_dir_path)

        reinitialize(repository_dir_path)

        mock_requests_post.assert_called_with(
            url=f"{api.get_base_api_url()}/reinitialize_repository",
            json=json.dumps(
                {
                    "repository": repository.to_dict(),
                    "repository_id": repository_id,
                },
                default=str,
            ),
        )

    def test_uninitialize_with_invalid_path(self) -> None:
        invalid_path: Path = self.test_temp_folder_path / "invalid_path"
        with self.assertRaises(dot_insight_dir.InvalidDotInsightDirectoryPathError):
            uninitialize(invalid_path)

    def test_uninitialize_with_valid_path(self) -> None:
        repository_dir_path = self.test_temp_folder_path
        dot_insight_dir_path: Path = (
            repository_dir_path / dot_insight_dir.get_dir_name()
        )
        repository_id = "123"
        dot_insight_dir.create(dot_insight_dir_path, repository_id)
        uninitialize(repository_dir_path)
        self.assertFalse(dot_insight_dir_path.is_dir())


if __name__ == "__main__":
    unittest.main()
