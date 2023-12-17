from pathlib import Path
from unittest.mock import patch, MagicMock
import json, tempfile, unittest

from insight_cli.repository.authenticator import Authenticator


class Testauthenticator(unittest.TestCase):
    def setUp(self):
        self._temp_dir = tempfile.TemporaryDirectory()
        self._temp_dir_path = Path(self._temp_dir.name)

    def tearDown(self):
        self._temp_dir.cleanup()

    def test_is_authenticator_data_instance_with_invalid_authenticator_data(
        self,
    ) -> None:
        invalid_authenticator_data = [
            [],
            {},
            {"repository_id": 4},
            {"repository_id": set()},
            {"repository_id": "hi", "extra_key": "extra_val"},
        ]

        for data in invalid_authenticator_data:
            self.assertFalse(Authenticator._is_authenticator_data_instance(data))

    def test_is_authenticator_data_instance_with_valid_authenticator_data(self) -> None:
        valid_authenticator_data = [
            {"repository_id": ""},
            {"repository_id": "123"},
        ]

        for data in valid_authenticator_data:
            self.assertTrue(Authenticator._is_authenticator_data_instance(data))

    def test_create_with_non_invalid_authenticator_data(self) -> None:
        authenticator = Authenticator(self._temp_dir_path)
        invalid_authenticator_data = {"repository_id": 123}
        self.assertFalse(authenticator.is_valid)

        with self.assertRaises(ValueError) as context_manager:
            authenticator.create(invalid_authenticator_data)
            self.assertEqual(
                context_manager.exception,
                f"{invalid_authenticator_data} is not valid authenticator data.",
            )

        self.assertFalse(authenticator.is_valid)

    @patch("insight_cli.api.ValidateRepositoryIdAPI.make_request")
    def test_create_with_valid_authenticator_data(
        self, mock_validate_repository_id_request
    ) -> None:
        authenticator = Authenticator(self._temp_dir_path)
        self.assertFalse(authenticator.is_valid)

        authenticator.create({"repository_id": "sample_repository_id_123"})
        mock_validate_repository_id_request.return_value = {
            "repository_id_is_valid": True
        }

        self.assertTrue(authenticator.is_valid)

    def test_data_with_invalid_authenticator_path(self) -> None:
        authenticator = Authenticator(self._temp_dir_path)
        with self.assertRaises(FileNotFoundError):
            authenticator.data

        self.assertFalse(authenticator.is_valid)

        with open(authenticator._path, "w") as file:
            file.write(str({"repository_id": 3}))

        with self.assertRaises(json.decoder.JSONDecodeError):
            authenticator.data

        with open(authenticator._path, "w") as file:
            file.write(json.dumps({"repository_id": 3}, indent=4))

        with self.assertRaises(ValueError):
            authenticator.data

        self.assertFalse(authenticator.is_valid)

    @patch("insight_cli.api.ValidateRepositoryIdAPI.make_request")
    def test_data_with_valid_authenticator_path(
        self, mock_validate_repository_id_request
    ) -> None:
        authenticator = Authenticator(self._temp_dir_path)
        authenticator_data = {"repository_id": "sample_repository_id_123"}
        authenticator.create(authenticator_data)
        mock_validate_repository_id_request.return_value = {
            "repository_id_is_valid": True
        }

        self.assertTrue(authenticator.is_valid)
        self.assertEqual(authenticator.data, authenticator_data)

    def test_is_valid_with_invalid_authenticator_path(self) -> None:
        authenticator = Authenticator(self._temp_dir_path)
        invalid_authenticator_data = {"repository_id": 3}

        self.assertFalse(authenticator.is_valid)

        with open(authenticator._path, "w") as file:
            file.write(str(invalid_authenticator_data))

        with open(authenticator._path, "w") as file:
            file.write(json.dumps(invalid_authenticator_data, indent=4))

        self.assertFalse(authenticator.is_valid)

    @patch("insight_cli.api.ValidateRepositoryIdAPI.make_request")
    def test_is_valid_with_invalid_repository_id(
        self, mock_validate_repository_id_request
    ) -> None:
        authenticator = Authenticator(self._temp_dir_path)
        authenticator_data = {"repository_id": "example"}

        mock_validate_repository_id_request.return_value = {
            "repository_id_is_valid": False
        }

        authenticator.create(authenticator_data)

        self.assertFalse(authenticator.is_valid)

    @patch("insight_cli.api.ValidateRepositoryIdAPI.make_request")
    def test_is_valid_with_valid_authenticator_path(
        self, mock_validate_repository_id_request
    ) -> None:
        authenticator = Authenticator(self._temp_dir_path)
        authenticator_data = {"repository_id": "example"}
        authenticator.create(authenticator_data)

        mock_validate_repository_id_request.return_value = {
            "repository_id_is_valid": True
        }

        self.assertTrue(authenticator.is_valid)


if __name__ == "__main__":
    unittest.main()
