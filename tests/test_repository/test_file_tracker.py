from datetime import datetime
from pathlib import Path
import json, os, tempfile, unittest


from insight_cli.repository.file_tracker import FileTracker


class TestFileTracker(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_dir_path = Path(self.temp_dir.name)

        # self.file_tracker_path = self.temp_dir_path / FileTracker(self.temp_dir_path)

        # with open(self.file_tracker_path, "w") as file:
        #     file.write(
        #         json.dumps(
        #             {
        #                 ".gitignore": 1702751393.8241253,
        #                 "LICENSE": 1701634560.0,
        #                 "README.md": 1702698126.458091,
        #                 "requirements.txt": 1701913276.0,
        #                 "setup.py": 1702696466.8386028,
        #             }
        #         )
        #     )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_create(self) -> None:
        file_paths = [
            Path(self.temp_dir_path / "file1"),
            Path(self.temp_dir_path / "file2"),
            Path(self.temp_dir_path / "file3"),
        ]

        for file_path in file_paths:
            file_path.touch()

        file_tracker = FileTracker(self.temp_dir_path)

        file_tracker.create(file_paths)

        self.assertEqual(
            file_tracker.tracked_file_modified_times,
            {
                Path(file_path): datetime.fromtimestamp(os.path.getmtime(file_path))
                for file_path in file_paths
            },
        )

    def change_file_paths(self) -> None:
        with open(self.temp_dir_path / FileTracker._FILE_NAME, "w") as file:
            file.write(
                json.dumps(
                    {
                        ".gitignore": 1702751393.8241253,
                        "LICENSE": 1701634560.0,
                        "README.md": 1702698126.458091,
                        "requirements.txt": 1701913276.0,
                        "setup.py": 1702696466.8386028,
                    }
                )
            )

        paths_to_add = [Path("file1"), Path("file2")]

        for path in paths_to_add:
            path.touch()

        paths_to_update = [Path("setup.py")]
        paths_to_delete = [Path("LICENSE")]

        file_tracker = FileTracker(self.temp_dir_path)

        file_tracker.change_file_paths(
            paths_to_add=paths_to_add,
            paths_to_update=paths_to_update,
            paths_to_delete=paths_to_delete,
        )

        new_file_paths = [
            Path(".gitignore"),
            Path("README.md"),
            Path("requirements.txt"),
            Path("file1"),
            Path("file2"),
            Path("setup.py"),
        ]

        self.assertEqual(
            file_tracker.tracked_file_modified_times,
            {
                Path(file_path): datetime.fromtimestamp(os.path.getmtime(file_path))
                for file_path in new_file_paths
            },
        )


if __name__ == "__main__":
    unittest.main()
