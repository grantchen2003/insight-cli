from pathlib import Path
from datetime import datetime
import tempfile, unittest

from insight_cli.utils.file_changes_detector import FileChangesDetector, File


class TestFileChangesDetector(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_dir_path = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_file_path_changes_with_no_changes(self) -> None:
        previous_files = {
            Path("file1.txt"): datetime(2023, 1, 1),
            Path("file2.txt"): datetime(2023, 1, 2),
            Path("file3.txt"): datetime(2023, 1, 4),
        }
        current_files = {
            Path("file1.txt"): datetime(2023, 1, 1),
            Path("file2.txt"): datetime(2023, 1, 2),
            Path("file3.txt"): datetime(2023, 1, 4),
        }

        file_changes_detector = FileChangesDetector(
            previous_file_modified_times=previous_files,
            current_file_modified_times=current_files,
        )

        self.assertEqual(
            file_changes_detector.file_path_changes,
            {"add": [], "update": [], "delete": []},
        )

    def test_file_path_changes_with_changes(self) -> None:
        previous_files = {
            Path("file1.txt"): datetime(2023, 1, 1),
            Path("file2.txt"): datetime(2023, 1, 2),
            Path("file3.txt"): datetime(2023, 1, 4),
        }
        current_files = {
            Path("file1.txt"): datetime(2023, 1, 3),
            Path("file2.txt"): datetime(2023, 1, 2),
            Path("file4.txt"): datetime(2023, 1, 4),
            Path("file5.txt"): datetime(2023, 1, 4),
        }

        file_changes_detector = FileChangesDetector(
            previous_file_modified_times=previous_files,
            current_file_modified_times=current_files,
        )

        self.assertSetEqual(
            set(file_changes_detector.file_path_changes["add"]),
            {Path("file4.txt"), Path("file5.txt")},
        )
        self.assertSetEqual(
            set(file_changes_detector.file_path_changes["update"]), {Path("file1.txt")}
        )
        self.assertSetEqual(
            set(file_changes_detector.file_path_changes["delete"]), {Path("file3.txt")}
        )

    def test_file_changes_no_changes(self) -> None:
        previous_files = {
            Path("file1.txt"): datetime(2023, 1, 1),
            Path("file2.txt"): datetime(2023, 1, 2),
            Path("file3.txt"): datetime(2023, 1, 4),
        }
        current_files = {
            Path("file1.txt"): datetime(2023, 1, 1),
            Path("file2.txt"): datetime(2023, 1, 2),
            Path("file3.txt"): datetime(2023, 1, 4),
        }

        file_changes_detector = FileChangesDetector(
            previous_file_modified_times=previous_files,
            current_file_modified_times=current_files,
        )

        self.assertEqual(
            file_changes_detector.file_changes, {"add": [], "update": [], "delete": []}
        )

    def test_file_changes_with_changes(self) -> None:
        with open(self.temp_dir_path / "file1.txt", "w") as file:
            file.write("yo1")

        with open(self.temp_dir_path / "file2.txt", "w") as file:
            file.write("yo2")

        with open(self.temp_dir_path / "file4.txt", "w") as file:
            file.write("yo4")

        with open(self.temp_dir_path / "file5.txt", "w") as file:
            file.write("yo5")

        previous_files = {
            Path(self.temp_dir_path / "file1.txt"): datetime(2023, 1, 1),
            Path(self.temp_dir_path / "file2.txt"): datetime(2023, 1, 2),
            Path(self.temp_dir_path / "file3.txt"): datetime(2023, 1, 4),
        }
        current_files = {
            Path(self.temp_dir_path / "file1.txt"): datetime(2023, 1, 3),
            Path(self.temp_dir_path / "file2.txt"): datetime(2023, 1, 2),
            Path(self.temp_dir_path / "file4.txt"): datetime(2023, 1, 4),
            Path(self.temp_dir_path / "file5.txt"): datetime(2023, 1, 4),
        }

        file_changes_detector = FileChangesDetector(
            previous_file_modified_times=previous_files,
            current_file_modified_times=current_files,
        )

        self.assertSetEqual(
            set(file_changes_detector.file_changes["add"]),
            {
                (str(self.temp_dir_path / "file5.txt"), b"yo5"),
                (str(self.temp_dir_path / "file4.txt"), b"yo4"),
            },
        )
        self.assertSetEqual(
            set(file_changes_detector.file_changes["update"]),
            {(str(self.temp_dir_path / "file1.txt"), b"yo1")},
        )
        self.assertSetEqual(
            set(file_changes_detector.file_changes["delete"]),
            {(str(self.temp_dir_path / "file3.txt"), b"")},
        )

    def test_no_files_changes_exist_with_no_changes(self) -> None:
        previous_files = {
            Path("file1.txt"): datetime(2023, 1, 1),
            Path("file2.txt"): datetime(2023, 1, 2),
            Path("file3.txt"): datetime(2023, 1, 4),
        }
        current_files = {
            Path("file1.txt"): datetime(2023, 1, 1),
            Path("file2.txt"): datetime(2023, 1, 2),
            Path("file3.txt"): datetime(2023, 1, 4),
        }

        file_changes_detector = FileChangesDetector(
            previous_file_modified_times=previous_files,
            current_file_modified_times=current_files,
        )

        self.assertTrue(file_changes_detector.no_files_changes_exist)
        
    def test_no_files_changes_exist_with_changes(self) -> None:
        previous_files = {
            Path("file1.txt"): datetime(2023, 1, 1),
            Path("file2.txt"): datetime(2023, 1, 2),
            Path("file3.txt"): datetime(2023, 1, 4),
        }
        current_files = {
            Path("file1.txt"): datetime(2023, 1, 1),
            Path("file2.txt"): datetime(2023, 1, 2),
            Path("file3.txt"): datetime(2023, 1, 4),
            Path("file5.txt"): datetime(2023, 1, 4),
        }

        file_changes_detector = FileChangesDetector(
            previous_file_modified_times=previous_files,
            current_file_modified_times=current_files,
        )

        self.assertFalse(file_changes_detector.no_files_changes_exist)


if __name__ == "__main__":
    unittest.main()
