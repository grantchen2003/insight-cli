from pathlib import Path
from unittest.mock import patch, PropertyMock
import tempfile, unittest

from insight_cli.repository import Repository, InvalidRepositoryError


class TestRepository(unittest.TestCase):
    def setUp(self):
        self._temp_dir = tempfile.TemporaryDirectory()
        self._temp_dir_path = Path(self._temp_dir.name)

    def tearDown(self):
        self._temp_dir.cleanup()

    @patch("insight_cli.api.ValidateRepositoryIdAPI.make_request")
    @patch("insight_cli.api.InitializeRepositoryAPI.make_request")
    def test_initialize_with_non_existing_repository(
        self,
        mock_initialize_repository_request,
        mock_make_validate_repository_id_request,
    ) -> None:
        mock_make_validate_repository_id_request.return_value = {
            "repository_id_is_valid": True
        }
        mock_initialize_repository_request.return_value = {"repository_id": "123"}
        repository = Repository(self._temp_dir_path)

        self.assertFalse(repository.is_valid)

        repository.initialize()

        mock_initialize_repository_request.assert_called_once()
        self.assertTrue(repository.is_valid)

    @patch("insight_cli.api.ValidateRepositoryIdAPI.make_request")
    @patch("insight_cli.api.InitializeRepositoryAPI.make_request")
    def test_initialize_with_existing_repository(
        self,
        mock_initialize_repository_request,
        mock_make_validate_repository_id_request,
    ) -> None:
        mock_make_validate_repository_id_request.return_value = {
            "repository_id_is_valid": True
        }
        mock_initialize_repository_request.return_value = {"repository_id": "123"}
        repository = Repository(self._temp_dir_path)

        self.assertFalse(repository.is_valid)

        repository.initialize()

        self.assertTrue(repository.is_valid)

        repository.initialize()

        self.assertTrue(repository.is_valid)

    def test_reinitialize_with_non_existing_repository(self) -> None:
        repository = Repository(self._temp_dir_path)

        with self.assertRaises(InvalidRepositoryError):
            repository.reinitialize()

    @patch("insight_cli.api.ValidateRepositoryIdAPI.make_request")
    def test_reinitialize_with_invalid_repository_id(
        self, mock_make_validate_repository_id_request
    ) -> None:
        mock_make_validate_repository_id_request.return_value = {
            "repository_id_is_valid": False
        }
        repository = Repository(self._temp_dir_path)

        with self.assertRaises(InvalidRepositoryError):
            repository.reinitialize()

    @patch("insight_cli.api.ReinitializeRepositoryAPI.make_request")
    @patch("insight_cli.api.ValidateRepositoryIdAPI.make_request")
    @patch("insight_cli.api.InitializeRepositoryAPI.make_request")
    def test_reinitialize_with_existing_repository(
        self,
        mock_initialize_repository_request,
        mock_make_validate_repository_id_request,
        mock_reinitialize_repository_request,
    ) -> None:
        mock_make_validate_repository_id_request.return_value = {
            "repository_id_is_valid": True
        }
        mock_initialize_repository_request.return_value = {"repository_id": "123"}
        repository = Repository(self._temp_dir_path)

        self.assertFalse(repository.is_valid)

        repository.initialize()

        self.assertTrue(repository.is_valid)

        Path(self._temp_dir_path / "new_file").touch()

        repository.reinitialize()

        self.assertTrue(repository.is_valid)
        mock_reinitialize_repository_request.assert_called_once()

    def test_uninitialize_with_non_existing_repository(self) -> None:
        repository = Repository(self._temp_dir_path)

        with self.assertRaises(InvalidRepositoryError):
            repository.uninitialize()

    @patch("insight_cli.api.UninitializeRepositoryAPI.make_request")
    @patch("insight_cli.api.ValidateRepositoryIdAPI.make_request")
    @patch("insight_cli.api.InitializeRepositoryAPI.make_request")
    def test_uninitialize_with_existing_repository(
        self,
        mock_initialize_repository_request,
        mock_make_validate_repository_id_request,
        mock_uninitialize_repository_request,
    ) -> None:
        mock_make_validate_repository_id_request.return_value = {
            "repository_id_is_valid": True
        }
        mock_initialize_repository_request.return_value = {"repository_id": "123"}
        repository = Repository(self._temp_dir_path)

        self.assertFalse(repository.is_valid)

        repository.initialize()

        self.assertTrue(repository.is_valid)

        repository.uninitialize()
        
        mock_uninitialize_repository_request.assert_called_once()

        self.assertFalse(repository.is_valid)

    def test_query_with_non_existing_repository(self) -> None:
        repository = Repository(self._temp_dir_path)
        query_string = "water"

        with self.assertRaises(InvalidRepositoryError):
            repository.query(query_string)

    @patch("insight_cli.api.QueryRepositoryAPI.make_request")
    @patch("insight_cli.api.ValidateRepositoryIdAPI.make_request")
    @patch("insight_cli.api.InitializeRepositoryAPI.make_request")
    def test_query_with_existing_repository(
        self,
        mock_initialize_repository_request,
        mock_make_validate_repository_id_request,
        mock_query_repository_request,
    ) -> None:
        mock_make_validate_repository_id_request.return_value = {
            "repository_id_is_valid": True
        }
        mock_initialize_repository_request.return_value = {"repository_id": "123"}
        mock_query_repository_request.return_value = []
        repository = Repository(self._temp_dir_path)
        query_string = "water"

        self.assertFalse(repository.is_valid)

        repository.initialize()

        self.assertTrue(repository.is_valid)

        self.assertEqual(repository.query(query_string), [])

        self.assertTrue(repository.is_valid)

    def test_is_valid_with_invalid_repository(self) -> None:
        repository = Repository(self._temp_dir_path)
        self.assertFalse(repository.is_valid)


if __name__ == "__main__":
    unittest.main()
