from datetime import datetime
import unittest

from insight_cli.utils.directory import Directory, File


class TestDirectory(unittest.TestCase):
    def test_add_file_with_one_file(self) -> None:
        file = File("example_file", datetime.now(), ["example_content"])

        directory = Directory("example_directory", datetime.now())
        directory.add_file(file)

        self.assertIn(file, directory._files)

    def test_add_file_with_two_files(self) -> None:
        file1 = File("example_file1", datetime.now(), ["example_content"])
        file2 = File("example_file2", datetime.now(), ["example_content"])

        directory = Directory("example_directory", datetime.now())
        directory.add_file(file1)
        directory.add_file(file2)

        self.assertIn(file1, directory._files)
        self.assertIn(file2, directory._files)

    def test_add_subdirectory_with_one_subdirectory(self) -> None:
        subdirectory = Directory("example_subdirectory", datetime.now())
        directory = Directory("example_directory", datetime.now())

        directory.add_subdirectory(subdirectory)

        self.assertIn(subdirectory, directory._subdirectories)

    def test_add_subdirectory_with_two_subdirectories(self) -> None:
        subdirectory1 = Directory("example_subdirectory1", datetime.now())
        subdirectory2 = Directory("example_subdirectory2", datetime.now())

        directory = Directory("example_directory", datetime.now())
        directory.add_subdirectory(subdirectory1)
        directory.add_subdirectory(subdirectory2)

        self.assertIn(subdirectory1, directory._subdirectories)
        self.assertIn(subdirectory2, directory._subdirectories)

    def test_to_dict_with_one_file_and_one_empty_subdirectory(self) -> None:
        file = File("test_file.txt", datetime.now(), [])
        subdirectory = Directory("example_subdirectory", datetime.now())

        directory = Directory("example_directory", datetime.now())
        directory.add_file(file)
        directory.add_subdirectory(subdirectory)

        expected_dict = {
            "name": "example_directory",
            "last_updated": datetime.now(),
            "files": [
                {
                    "name": "test_file.txt",
                    "last_updated": datetime.now(),
                    "content": [],
                }
            ],
            "subdirectories": [
                {
                    "name": "example_subdirectory",
                    "last_updated": datetime.now(),
                    "files": [],
                    "subdirectories": [],
                }
            ],
        }

        self.assertEqual(directory.to_dict(), expected_dict)


if __name__ == "__main__":
    unittest.main()
