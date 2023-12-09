from pathlib import Path
import tempfile, unittest

from insight_cli.utils.directory import Directory, DirectoryDict
from insight_cli.utils.file import File


class TestDirectory(unittest.TestCase):
    def setUp(self):
        self._temp_dir = tempfile.TemporaryDirectory()
        self._temp_dir_path = Path(self._temp_dir.name)

    def tearDown(self):
        self._temp_dir.cleanup()

    def test_create_in_file_system_with_empty_dir_dict(self) -> None:
        dir_dict: DirectoryDict = {
            "path": self._temp_dir_path / "empty dir name",
            "files": [],
            "subdirectories": [],
        }

        Directory.create_in_file_system(dir_dict)

        self.assertEqual(
            Directory.create_from_path(dir_dict["path"]).to_directory_dict(), dir_dict
        )

    def test_create_in_file_system_with_non_empty_dir_dict(self) -> None:
        dir_dict: DirectoryDict = {
            "path": self._temp_dir_path / "non empty dir name",
            "files": [
                {
                    "path": self._temp_dir_path / "non empty dir name" / "file1_name",
                    "lines": [],
                },
                {
                    "path": self._temp_dir_path / "non empty dir name" / "file2_name",
                    "lines": ["hello"],
                },
            ],
            "subdirectories": [
                {
                    "path": self._temp_dir_path
                    / "non empty dir name"
                    / "subdir dir name",
                    "files": [
                        {
                            "path": self._temp_dir_path
                            / "non empty dir name"
                            / "subdir dir name"
                            / "file3_name",
                            "lines": ["yo", "whats", "good"],
                        },
                    ],
                    "subdirectories": [],
                }
            ],
        }

        Directory.create_in_file_system(dir_dict)

        self.assertEqual(
            Directory.create_from_path(dir_dict["path"]).to_directory_dict(), dir_dict
        )

    def test_create_from_path_with_path_of_empty_dir(self) -> None:
        empty_dir_path = self._temp_dir_path / "empty_dir"
        empty_dir_path.mkdir()

        directory = Directory.create_from_path(empty_dir_path)

        self.assertEqual(directory._path, self._temp_dir_path / "empty_dir")
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
            "path": self._temp_dir_path / "directory",
            "files": [
                {
                    "path": self._temp_dir_path / "directory" / "directory_file",
                    "lines": ["hello there"],
                }
            ],
            "subdirectories": [
                {
                    "path": self._temp_dir_path / "directory" / "subdirectory",
                    "files": [
                        {
                            "path": self._temp_dir_path
                            / "directory"
                            / "subdirectory"
                            / "subdirectory_file",
                            "lines": ["hello there2"],
                        }
                    ],
                    "subdirectories": [],
                }
            ],
        }

        self.assertEqual(directory.to_directory_dict(), expected_dict)

    def test_create_from_path_with_invalid_ignorable_names(self) -> None:
        dir_dict: DirectoryDict = {
            "path": self._temp_dir_path / "non empty dir name",
            "files": [
                {
                    "path": self._temp_dir_path / "non empty dir name" / "file1_name",
                    "lines": [],
                }
            ],
            "subdirectories": [],
        }

        Directory.create_in_file_system(dir_dict)

        with self.assertRaises(ValueError):
            Directory.create_from_path(dir_dict["path"], ["file1_name", "*."])

    def test_create_from_path_with_valid_ignorable_names(self) -> None:
        dir_dict: DirectoryDict = {
            "path": self._temp_dir_path / "non empty dir name",
            "files": [
                {
                    "path": self._temp_dir_path / "non empty dir name" / "file1_name",
                    "lines": [],
                },
                {
                    "path": self._temp_dir_path / "non empty dir name" / "file2_name",
                    "lines": ["hello"],
                },
            ],
            "subdirectories": [
                {
                    "path": self._temp_dir_path
                    / "non empty dir name"
                    / "subdir dir name",
                    "files": [
                        {
                            "path": self._temp_dir_path
                            / "non empty dir name"
                            / "subdir dir name"
                            / "file3_name",
                            "lines": ["yo", "whats", "good"],
                        },
                    ],
                    "subdirectories": [],
                }
            ],
        }

        Directory.create_in_file_system(dir_dict)

        self.assertEqual(
            Directory.create_from_path(
                dir_dict["path"], ["file1_name", "subdir dir name"]
            ).to_directory_dict(),
            {
                "path": self._temp_dir_path / "non empty dir name",
                "files": [
                    {
                        "path": self._temp_dir_path
                        / "non empty dir name"
                        / "file2_name",
                        "lines": ["hello"],
                    }
                ],
                "subdirectories": [],
            },
        )

    def test_add_file_with_one_empty_file(self) -> None:
        directory = Directory("example_directory")
        file = File("empty_file", [])

        directory.add_file(file)

        self.assertIn(file, directory._files)

    def test_add_file_with_one_non_empty_file(self) -> None:
        directory = Directory("example_directory")
        file = File("non_empty_file", ["example_lines"])

        directory.add_file(file)

        self.assertIn(file, directory._files)

    def test_add_file_with_two_empty_files(self) -> None:
        directory = Directory("example_directory")
        file1 = File("empty_file1", [])
        file2 = File("empty_file2", [])

        directory.add_file(file1)
        directory.add_file(file2)

        self.assertIn(file1, directory._files)
        self.assertIn(file2, directory._files)

    def test_add_file_with_one_empty_file_and_one_non_empty_file(self) -> None:
        directory = Directory("example_directory")
        file1 = File("empty_file", [])
        file2 = File("non_empty_file", ["example_lines"])

        directory.add_file(file1)
        directory.add_file(file2)

        self.assertIn(file1, directory._files)
        self.assertIn(file2, directory._files)

    def test_add_file_with_two_non_empty_files(self) -> None:
        directory = Directory("example_directory")
        file1 = File("non_empty_file1", ["example_lines"])
        file2 = File("non_empty_file2", ["example_lines"])

        directory.add_file(file1)
        directory.add_file(file2)

        self.assertIn(file1, directory._files)
        self.assertIn(file2, directory._files)

    def test_add_subdirectory_with_one_empty_subdirectory(self) -> None:
        directory = Directory("directory")
        subdirectory = Directory("empty_subdirectory")

        directory.add_subdirectory(subdirectory)

        self.assertIn(subdirectory, directory._subdirectories)

    def test_add_subdirectory_with_two_empty_subdirectories(self) -> None:
        directory = Directory("directory")
        subdirectory1 = Directory("empty_subdirectory1")
        subdirectory2 = Directory("empty_subdirectory2")

        directory.add_subdirectory(subdirectory1)
        directory.add_subdirectory(subdirectory2)

        self.assertIn(subdirectory1, directory._subdirectories)
        self.assertIn(subdirectory2, directory._subdirectories)

    def test_to_dict_with_one_empty_file_and_one_empty_subdirectory(self) -> None:
        directory = Directory(self._temp_dir_path / "directory")
        directory.add_file(File(self._temp_dir_path / "directory" / "empty_file", []))
        directory.add_subdirectory(
            Directory(self._temp_dir_path / "directory" / "empty_subdirectory")
        )

        expected_dict = {
            "path": self._temp_dir_path / "directory",
            "files": [
                {
                    "path": self._temp_dir_path / "directory" / "empty_file",
                    "lines": [],
                }
            ],
            "subdirectories": [
                {
                    "path": self._temp_dir_path / "directory" / "empty_subdirectory",
                    "files": [],
                    "subdirectories": [],
                }
            ],
        }

        self.assertEqual(directory.to_directory_dict(), expected_dict)


if __name__ == "__main__":
    unittest.main()
