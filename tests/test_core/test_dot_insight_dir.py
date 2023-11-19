from pathlib import Path
from unittest.mock import patch, Mock
import json
import os
import shutil
import unittest

from src.core.api import get_base_api_url
from src.core.dot_insight_dir import (
    InvalidDotInsightDirectoryPathError,
    get_dir_name,
    get_repository_id,
    get_config_file_name,
    is_valid,
    create,
    delete,
)


class TestDotInsightDir(unittest.TestCase):
    def setUp(self) -> None:
        self.test_temp_folder_path = Path("./tests/test_core/temp_test_dot_insight_dir")
        if not os.path.exists(self.test_temp_folder_path):
            os.makedirs(self.test_temp_folder_path)

    def tearDown(self):
        shutil.rmtree(self.test_temp_folder_path)

    def test_get_dir_name(self) -> None:
        return self.assertEqual(get_dir_name(), ".insight")

    def test_get_config_file_name(self) -> None:
        return self.assertEqual(get_config_file_name(), "config.json")

    def test_get_repository_id_with_invalid_path(self) -> None:
        dot_insight_dir_path = Path()
        with self.assertRaises(FileNotFoundError):
            get_repository_id(dot_insight_dir_path)

    def test_get_repository_id_with_no_config_json_file(self) -> None:
        dot_insight_dir_path: Path = self.test_temp_folder_path / get_dir_name()
        os.makedirs(dot_insight_dir_path)
        with self.assertRaises(FileNotFoundError):
            get_repository_id(dot_insight_dir_path)

    def test_get_repository_id_with_empty_config_json_file(self) -> None:
        dot_insight_dir_path: Path = self.test_temp_folder_path / get_dir_name()
        config_json_file_path: Path = dot_insight_dir_path / get_config_file_name()
        config_json_file_content = ""

        os.makedirs(dot_insight_dir_path)

        with open(config_json_file_path, "w") as config_json_file:
            config_json_file.write(config_json_file_content)

        with self.assertRaises(json.decoder.JSONDecodeError):
            get_repository_id(dot_insight_dir_path)

    def test_get_repository_id_with_non_json_config_json_file(self) -> None:
        dot_insight_dir_path: Path = self.test_temp_folder_path / get_dir_name()
        config_json_file_path: Path = dot_insight_dir_path / get_config_file_name()
        config_json_file_content = "water"

        os.makedirs(dot_insight_dir_path)

        with open(config_json_file_path, "w") as config_json_file:
            config_json_file.write(config_json_file_content)

        with self.assertRaises(json.decoder.JSONDecodeError):
            get_repository_id(dot_insight_dir_path)

    def test_get_repository_id_with_missing_keys_config_json_file(self) -> None:
        dot_insight_dir_path: Path = self.test_temp_folder_path / get_dir_name()
        config_json_file_path: Path = dot_insight_dir_path / get_config_file_name()
        config_json_file_content = {"invalid_key": "invalid_value"}

        os.makedirs(dot_insight_dir_path)

        with open(config_json_file_path, "w") as config_json_file:
            json.dump(config_json_file_content, config_json_file)

        with self.assertRaises(KeyError):
            get_repository_id(dot_insight_dir_path)

    def test_get_repository_id_with_valid_config_json_file(self) -> None:
        dot_insight_dir_path: Path = self.test_temp_folder_path / get_dir_name()
        config_json_file_path: Path = dot_insight_dir_path / get_config_file_name()
        config_json_file_content = {"repository_id": "123"}

        os.makedirs(dot_insight_dir_path)

        with open(config_json_file_path, "w") as config_json_file:
            json.dump(config_json_file_content, config_json_file)

        self.assertEqual(
            get_repository_id(dot_insight_dir_path),
            config_json_file_content["repository_id"],
        )

    def test_is_valid_with_invalid_dir_name(self) -> None:
        dot_insight_dir_path: Path = self.test_temp_folder_path / "invalid_dir_name"
        os.makedirs(dot_insight_dir_path)
        self.assertFalse(is_valid(dot_insight_dir_path))

    def test_is_valid_with_invalid_config_json(self) -> None:
        dot_insight_dir_path: Path = self.test_temp_folder_path / get_dir_name()
        config_json_file_path: Path = dot_insight_dir_path / get_config_file_name()
        config_json_file_content = {"water": "123"}

        os.makedirs(dot_insight_dir_path)

        with open(config_json_file_path, "w") as config_json_file:
            json.dump(config_json_file_content, config_json_file)

        self.assertFalse(is_valid(dot_insight_dir_path))

    @patch("requests.post")
    def test_is_valid_with_invalid_repository_id(self, mock_request_post) -> None:
        dot_insight_dir_path: Path = self.test_temp_folder_path / get_dir_name()
        config_json_file_path: Path = dot_insight_dir_path / get_config_file_name()
        config_json_file_content = {"repository_id": "123"}

        os.makedirs(dot_insight_dir_path)

        with open(config_json_file_path, "w") as config_json_file:
            json.dump(config_json_file_content, config_json_file)

        mock_response = Mock()
        mock_response.json.return_value = {"repository_id_is_valid": False}
        mock_request_post.return_value = mock_response

        self.assertFalse(is_valid(dot_insight_dir_path))
        mock_request_post.assert_called_with(
            url=f"{get_base_api_url()}/validate_repository_id",
            json=json.dumps({"repository_id": "123"}),
        )

    @patch("requests.post")
    def test_is_valid_with_valid_dir(self, mock_request_post) -> None:
        dot_insight_dir_path: Path = self.test_temp_folder_path / get_dir_name()
        config_json_file_path: Path = dot_insight_dir_path / get_config_file_name()
        config_json_file_content = {"repository_id": "123"}

        os.makedirs(dot_insight_dir_path)

        with open(config_json_file_path, "w") as config_json_file:
            json.dump(config_json_file_content, config_json_file)

        mock_response = Mock()
        mock_response.json.return_value = {"repository_id_is_valid": True}
        mock_request_post.return_value = mock_response

        self.assertTrue(is_valid(dot_insight_dir_path))
        mock_request_post.assert_called_with(
            url=f"{get_base_api_url()}/validate_repository_id",
            json=json.dumps({"repository_id": "123"}),
        )

    @patch("requests.post")
    def test_create(self, mock_request_post) -> None:
        dot_insight_dir_path: Path = self.test_temp_folder_path / get_dir_name()
        repository_id = "123"

        mock_response = Mock()
        mock_response.json.return_value = {"repository_id_is_valid": True}
        mock_request_post.return_value = mock_response

        create(dot_insight_dir_path, repository_id)

        self.assertTrue(is_valid(dot_insight_dir_path))

        mock_request_post.assert_called_with(
            url=f"{get_base_api_url()}/validate_repository_id",
            json=json.dumps({"repository_id": repository_id}),
        )

    def test_delete_with_invalid_path(self) -> None:
        dot_insight_dir_path: Path = self.test_temp_folder_path / get_dir_name()
        with self.assertRaises(InvalidDotInsightDirectoryPathError):
            delete(dot_insight_dir_path)

    def test_delete_with_valid_path(self) -> None:
        dot_insight_dir_path: Path = self.test_temp_folder_path / get_dir_name()
        repository_id = "123"

        create(dot_insight_dir_path, repository_id)

        delete(dot_insight_dir_path)

        self.assertFalse(dot_insight_dir_path.is_dir())


if __name__ == "__main__":
    unittest.main()
