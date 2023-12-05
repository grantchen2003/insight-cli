from datetime import datetime
from pathlib import Path
import tempfile
import unittest

from insight_cli.utils.directory import Directory, File


class TestDirectory(unittest.TestCase):
    def setUp(self):
        self._temp_dir = tempfile.TemporaryDirectory()
        self._temp_dir_path = Path(self._temp_dir.name)

    def tearDown(self):
        self._temp_dir.cleanup()

    def test_create_from_path_with_path_of_empty_dir(self) -> None:
        empty_dir_path = self._temp_dir_path / "empty_dir"
        empty_dir_path.mkdir()

        directory = Directory.create_from_path(empty_dir_path)

        self.assertEqual(directory._name, "empty_dir")
        self.assertEqual(
            directory._last_updated,
            datetime.fromtimestamp(empty_dir_path.stat().st_mtime),
        )
        self.assertEqual(len(directory._files), 0)
        self.assertEqual(len(directory._subdirectories), 0)

    def test_create_from_path_with_path_of_non_empty_dir(self) -> None:
        dir_path = self._temp_dir_path / "directory"
        dir_file_path = dir_path / "directory_file"
        subdir_path = dir_path / "subdirectory"
        subdir_file_path = subdir_path / "subdirectory_file"
        dir_path.mkdir()
        dir_file_path.touch()
        with dir_file_path.open("w") as dir_file:
            dir_file.write("hello there")
        subdir_path.mkdir()
        subdir_file_path.touch()
        with subdir_file_path.open("w") as subdir_file:
            subdir_file.write("hello there2")

        directory = Directory.create_from_path(dir_path)

        expected_dict = {
            "name": "directory",
            "last_updated": datetime.fromtimestamp(dir_path.stat().st_mtime),
            "files": [
                {
                    "name": "directory_file",
                    "last_updated": datetime.fromtimestamp(
                        dir_file_path.stat().st_mtime
                    ),
                    "content": ["hello there"],
                }
            ],
            "subdirectories": [
                {
                    "name": "subdirectory",
                    "last_updated": datetime.fromtimestamp(subdir_path.stat().st_mtime),
                    "files": [
                        {
                            "name": "subdirectory_file",
                            "last_updated": datetime.fromtimestamp(
                                subdir_file_path.stat().st_mtime
                            ),
                            "content": ["hello there2"],
                        }
                    ],
                    "subdirectories": [],
                }
            ],
        }

        self.assertEqual(directory.to_dict(), expected_dict)

    def test_add_file_with_one_empty_file(self) -> None:
        directory = Directory("example_directory", datetime.now())
        file = File("empty_file", datetime.now(), [])

        directory.add_file(file)

        self.assertIn(file, directory._files)

    def test_add_file_with_one_non_empty_file(self) -> None:
        directory = Directory("example_directory", datetime.now())
        file = File("non_empty_file", datetime.now(), ["example_content"])

        directory.add_file(file)

        self.assertIn(file, directory._files)

    def test_add_file_with_two_empty_files(self) -> None:
        directory = Directory("example_directory", datetime.now())
        file1 = File("empty_file1", datetime.now(), [])
        file2 = File("empty_file2", datetime.now(), [])

        directory.add_file(file1)
        directory.add_file(file2)

        self.assertIn(file1, directory._files)
        self.assertIn(file2, directory._files)

    def test_add_file_with_one_empty_file_and_one_non_empty_file(self) -> None:
        directory = Directory("example_directory", datetime.now())
        file1 = File("empty_file", datetime.now(), [])
        file2 = File("non_empty_file", datetime.now(), ["example_content"])

        directory.add_file(file1)
        directory.add_file(file2)

        self.assertIn(file1, directory._files)
        self.assertIn(file2, directory._files)

    def test_add_file_with_two_non_empty_files(self) -> None:
        directory = Directory("example_directory", datetime.now())
        file1 = File("non_empty_file1", datetime.now(), ["example_content"])
        file2 = File("non_empty_file2", datetime.now(), ["example_content"])

        directory.add_file(file1)
        directory.add_file(file2)

        self.assertIn(file1, directory._files)
        self.assertIn(file2, directory._files)

    def test_add_subdirectory_with_one_empty_subdirectory(self) -> None:
        directory = Directory("directory", datetime.now())
        subdirectory = Directory("empty_subdirectory", datetime.now())

        directory.add_subdirectory(subdirectory)

        self.assertIn(subdirectory, directory._subdirectories)

    def test_add_subdirectory_with_two_empty_subdirectories(self) -> None:
        directory = Directory("directory", datetime.now())
        subdirectory1 = Directory("empty_subdirectory1", datetime.now())
        subdirectory2 = Directory("empty_subdirectory2", datetime.now())

        directory.add_subdirectory(subdirectory1)
        directory.add_subdirectory(subdirectory2)

        self.assertIn(subdirectory1, directory._subdirectories)
        self.assertIn(subdirectory2, directory._subdirectories)

    def test_to_dict_with_one_empty_file_and_one_empty_subdirectory(self) -> None:
        directory = Directory("directory", datetime.now())
        directory.add_file(File("empty_file", datetime.now(), []))
        directory.add_subdirectory(Directory("empty_subdirectory", datetime.now()))

        expected_dict = {
            "name": "directory",
            "last_updated": datetime.now(),
            "files": [
                {
                    "name": "empty_file",
                    "last_updated": datetime.now(),
                    "content": [],
                }
            ],
            "subdirectories": [
                {
                    "name": "empty_subdirectory",
                    "last_updated": datetime.now(),
                    "files": [],
                    "subdirectories": [],
                }
            ],
        }

        self.assertEqual(directory.to_dict(), expected_dict)


if __name__ == "__main__":
    unittest.main()
