from pathlib import Path
from unittest.mock import patch, Mock
import json, tempfile, unittest

from insight_cli.repository.config_file import ConfigFile, ConfigFileData, InvalidConfigFileDataError


class TestConfigFile(unittest.TestCase):
    def setUp(self):
        self._temp_dir = tempfile.TemporaryDirectory()
        self._temp_dir_path = Path(self._temp_dir.name)

    def tearDown(self):
        self._temp_dir.cleanup()

    def test_is_config_file_data_instance_with_invalid_config_file_data(self) -> None:
        invalid_config_files_data = [
            [],
            {},
            {"repository_id": 4},
            {"repository_id": set()},
            {"repository_id": "hi", "extra_key": "extra_val"},
        ]

        for invalid_config_file_data in invalid_config_files_data:
            self.assertFalse(
                ConfigFile._is_config_file_data_instance(invalid_config_file_data)
            )

    def test_is_config_file_data_instance_with_valid_config_file_data(self) -> None:
        valid_config_files_data = [
            {"repository_id": ""},
            {"repository_id": "123"},
        ]

        for valid_config_file_data in valid_config_files_data:
            self.assertTrue(
                ConfigFile._is_config_file_data_instance(valid_config_file_data)
            )

    def test_create_with_non_invalid_config_file_data(self) -> None:
        config_file = ConfigFile(self._temp_dir_path)
        config_file_data = {"repository_id": 123}
        self.assertFalse(config_file.is_valid)

        with self.assertRaises(InvalidConfigFileDataError) as context_manager:
            config_file.create(config_file_data)
            self.assertEqual(
                context_manager.exception,
                f"{config_file_data} is not valid config file data."
            )

        self.assertFalse(config_file.is_valid)

    @patch("insight_cli.api.API.make_validate_repository_id_request")
    def test_create_with_valid_config_file_data(self, mock_validate_repository_id_request) -> None:
        config_file = ConfigFile(self._temp_dir_path)
        config_file_data: ConfigFileData = {
            "repository_id": "sample_repository_id_123"
        }
        self.assertFalse(config_file.is_valid)

        config_file.create(config_file_data)
        mock_validate_repository_id_request.return_value = {"repository_id_is_valid": True}

        self.assertTrue(config_file.is_valid)

    def test_data_with_invalid_config_file_path(self) -> None:
        config_file = ConfigFile(self._temp_dir_path)
        invalid_config_file_data = {"repository_id": 3}

        with self.assertRaises(FileNotFoundError):
            config_file.data

        self.assertFalse(config_file.is_valid)

        with open(config_file._path, "w") as file:
            file.write(str(invalid_config_file_data))

        with self.assertRaises(json.decoder.JSONDecodeError):
            config_file.data

        with open(config_file._path, "w") as file:
            file.write(json.dumps(invalid_config_file_data, indent=4))

        with self.assertRaises(InvalidConfigFileDataError):
            config_file.data

        self.assertFalse(config_file.is_valid)

    @patch("insight_cli.api.API.make_validate_repository_id_request")
    def test_data_with_valid_config_file_path(self, mock_validate_repository_id_request) -> None:
        config_file = ConfigFile(self._temp_dir_path)
        config_file_data: ConfigFileData = {
            "repository_id": "sample_repository_id_123"
        }
        config_file.create(config_file_data)
        mock_validate_repository_id_request.return_value = {"repository_id_is_valid": True}

        self.assertTrue(config_file.is_valid)
        self.assertEqual(config_file.data, config_file_data)

    def test_is_valid_with_invalid_config_file_path(self) -> None:
        config_file = ConfigFile(self._temp_dir_path)
        invalid_config_file_data = {"repository_id": 3}

        self.assertFalse(config_file.is_valid)

        with open(config_file._path, "w") as file:
            file.write(str(invalid_config_file_data))

        with open(config_file._path, "w") as file:
            file.write(json.dumps(invalid_config_file_data, indent=4))

        self.assertFalse(config_file.is_valid)

    @patch("insight_cli.api.API.make_validate_repository_id_request")
    def test_is_valid_with_invalid_repository_id(self, mock_validate_repository_id_request) -> None:
        config_file = ConfigFile(self._temp_dir_path)
        config_file_data = {"repository_id": "example"}

        mock_response = Mock()
        mock_response.json.return_value = {"repository_id_is_valid": False}
        mock_validate_repository_id_request.return_value = mock_response

        config_file.create(config_file_data)

        self.assertFalse(config_file.is_valid)

    @patch("insight_cli.api.API.make_validate_repository_id_request")
    def test_is_valid_with_valid_config_file_path(self, mock_validate_repository_id_request) -> None:
        config_file = ConfigFile(self._temp_dir_path)
        config_file_data = {"repository_id": "example"}
        config_file.create(config_file_data)

        mock_validate_repository_id_request.return_value = {"repository_id_is_valid": True}

        self.assertTrue(config_file.is_valid)


if __name__ == "__main__":
    unittest.main()
