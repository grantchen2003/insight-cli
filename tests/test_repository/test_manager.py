import unittest
from unittest.mock import patch, MagicMock, PropertyMock
from pathlib import Path
from datetime import datetime
from tempfile import TemporaryDirectory
from insight_cli.repository.manager import Manager


class TestManager(unittest.TestCase):
    def setUp(self):
        self.temp_dir = TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    @patch("insight_cli.repository.authenticator.Authenticator.create")
    @patch("insight_cli.repository.file_tracker.FileTracker.create")
    def test_create(self, mock_file_tracker_create, mock_authenticator_create):
        repository_id = "test_repo_id"
        nested_repository_file_paths = [
            Path(self.temp_dir.name, "file1"),
            Path(self.temp_dir.name, "file2"),
        ]

        manager = Manager(Path(self.temp_dir.name))
        manager.create(repository_id, nested_repository_file_paths)
        mock_authenticator_create.assert_called_once_with(
            {"repository_id": repository_id}
        )
        mock_file_tracker_create.assert_called_once_with(nested_repository_file_paths)

    @patch("insight_cli.repository.file_tracker.FileTracker.change_file_paths")
    def test_update(self, mock_change_file_paths):
        repository_file_changes = {
            "add": [self.temp_dir.name + "/file3"],
            "update": [self.temp_dir.name + "/file1"],
            "delete": [self.temp_dir.name + "/file2"],
        }
        manager = Manager(Path(self.temp_dir.name))
        manager.update(repository_file_changes)
        mock_change_file_paths.assert_called_once_with(
            paths_to_add=[Path(self.temp_dir.name + "/file3")],
            paths_to_update=[Path(self.temp_dir.name + "/file1")],
            paths_to_delete=[Path(self.temp_dir.name + "/file2")],
        )

    def test_delete(self):
        manager = Manager(Path(self.temp_dir.name))
        manager.create("", [])
        manager.delete()
        self.assertFalse(Path(manager._path).exists())

    @patch(
        "insight_cli.repository.authenticator.Authenticator.is_valid",
        new_callable=PropertyMock,
        return_value=True,
    )
    def test_is_valid(self, mock_is_valid):
        manager = Manager(Path(self.temp_dir.name))
        self.assertTrue(manager.is_valid)
        mock_is_valid.assert_called_once()

    @patch(
        "insight_cli.repository.authenticator.Authenticator.data",
        new_callable=PropertyMock,
        return_value={"repository_id": "123"},
    )
    def test_repository_id(self, mock_authenticator_data):
        manager = Manager(Path(self.temp_dir.name))
        self.assertEqual(manager.repository_id, "123")
        mock_authenticator_data.assert_called_once()

    @patch(
        "insight_cli.repository.file_tracker.FileTracker.tracked_file_modified_times",
        new_callable=PropertyMock,
        return_value={},
    )
    def test_tracked_file_modified_times(self, mock_tracked_file_modified_times):
        manager = Manager(Path(self.temp_dir.name))
        self.assertEqual(manager.tracked_file_modified_times, {})
        mock_tracked_file_modified_times.assert_called_once()


if __name__ == "__main__":
    unittest.main()
