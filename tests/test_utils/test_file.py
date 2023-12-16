from pathlib import Path
import tempfile, unittest

from insight_cli.utils.file import File


class TestFileClass(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_dir_path = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_singleton_pattern(self):
        file_path = self.temp_dir_path / "test_file_1.txt"

        self.assertIs(File(file_path), File(file_path))

    def test_path(self):
        file_path = self.temp_dir_path / "test_file_1.txt"

        self.assertIs(File(file_path).path, file_path)

    def test_content_with_existing_file(self):
        file_path = self.temp_dir_path / "test_file_1.txt"
        content = b"Hello, World!"
        with open(file_path, "wb") as file:
            file.write(content)

        self.assertEqual(File(file_path).content, content)

    def test_content_with_non_existing_file(self):
        file_path = self.temp_dir_path / "test_file_1.txt"

        self.assertEqual(File(file_path).content, b"")


if __name__ == "__main__":
    unittest.main()
