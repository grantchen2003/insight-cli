from pathlib import Path
from unittest.mock import call, patch, PropertyMock
import tempfile, unittest

from insight_cli.repository.config_file import InvalidConfigFileDataError
from insight_cli.repository.core_dir import CoreDir


class TestCoreDir(unittest.TestCase):
    def setUp(self):
        self._temp_dir = tempfile.TemporaryDirectory()
        self._temp_dir_path = Path(self._temp_dir.name)

    def tearDown(self):
        self._temp_dir.cleanup()

    @patch("insight_cli.repository.config_file.ConfigFile.create")
    def test_create_with_invalid_repository_id(self, mock_create) -> None:
        core_dir = CoreDir(self._temp_dir_path)
        invalid_repository_id = 123

        mock_create.side_effect = InvalidConfigFileDataError({
            "repository_id": invalid_repository_id
        })

        with self.assertRaises(InvalidConfigFileDataError):
            core_dir.create(invalid_repository_id)

        mock_create.assert_called_once_with({
            "repository_id": invalid_repository_id
        })

    @patch("insight_cli.repository.config_file.ConfigFile.create")
    def test_create_with_valid_repository_id(self, mock_create) -> None:
        core_dir = CoreDir(self._temp_dir_path)
        repository_id = "123"

        core_dir.create(repository_id)

        mock_create.assert_called_once_with({
            "repository_id": repository_id
        })

    @patch("insight_cli.repository.config_file.ConfigFile.create")
    def test_create_with_existing_core_dir(self, mock_create) -> None:
        core_dir = CoreDir(self._temp_dir_path)

        for repository_id in ["123", "456"]:
            core_dir.create(repository_id)
            mock_create.assert_has_calls([call({
                "repository_id": repository_id
            })])

    @patch("insight_cli.repository.config_file.ConfigFile.is_valid", new_callable=PropertyMock)
    def test_delete_with_non_existing_core_dir(self, mock_is_valid) -> None:
        mock_is_valid.return_value = False
        core_dir = CoreDir(self._temp_dir_path)
        self.assertFalse(core_dir.is_valid)
        repository_id = "123"
        core_dir.create(repository_id)
        mock_is_valid.return_value = True
        self.assertTrue(core_dir.is_valid)
        self.assertEqual(core_dir.repository_id, repository_id)

    @patch("insight_cli.repository.config_file.ConfigFile.is_valid", new_callable=PropertyMock)
    def test_delete_with_existing_core_dir(self, mock_is_valid) -> None:
        mock_is_valid.return_value = False
        core_dir = CoreDir(self._temp_dir_path)
        self.assertFalse(core_dir.is_valid)

        for repository_id in ["123", "456"]:
            mock_is_valid.return_value = True
            core_dir.create(repository_id)
            self.assertTrue(core_dir.is_valid)
            self.assertEqual(core_dir.repository_id, repository_id)

    @patch("insight_cli.repository.config_file.ConfigFile.is_valid", new_callable=PropertyMock, return_value=False)
    def test_is_valid_with_invalid_config_file(self, mock_is_valid) -> None:
        core_dir = CoreDir(self._temp_dir_path)
        self.assertFalse(core_dir.is_valid)
        mock_is_valid.assert_called_once()

    @patch("insight_cli.repository.config_file.ConfigFile.is_valid", new_callable=PropertyMock, return_value=True)
    def test_is_valid_with_valid_config_file(self, mock_is_valid) -> None:
        core_dir = CoreDir(self._temp_dir_path)
        repository_id = "123"
        core_dir.create(repository_id)
        self.assertTrue(core_dir.is_valid)
        mock_is_valid.assert_called_once()

    @patch("insight_cli.repository.config_file.ConfigFile.is_valid", new_callable=PropertyMock, return_value=False)
    def test_repository_id_with_invalid_config_file(self, mock_is_valid) -> None:
        core_dir = CoreDir(self._temp_dir_path)
        self.assertFalse(core_dir.is_valid)
        mock_is_valid.assert_called_once()

        with self.assertRaises(FileNotFoundError):
            core_dir.repository_id

    def test_repository_id_with_valid_config_file(self) -> None:
        core_dir = CoreDir(self._temp_dir_path)
        repository_id = "123"
        core_dir.create(repository_id)

        self.assertEqual(core_dir.repository_id, repository_id)


if __name__ == "__main__":
    unittest.main()
