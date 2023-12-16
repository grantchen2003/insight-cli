from datetime import datetime
from pathlib import Path
import os, tempfile, unittest

from insight_cli.utils.directory import Directory, File


class TestDirectory(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_dir_path = Path(self.temp_dir.name)

        files = [
            ("file1.txt", "content1"),
            ("file2.txt", "content2"),
            ("subdir/file3.txt", "content3"),
            ("subdir/file4.txt", "content4"),
            ("subdir/file5.txt", "content5"),
            ("subdir1/file3.txt", "content6"),
        ]

        for file_path, file_content in files:
            (self.temp_dir_path / file_path).parent.mkdir(parents=True, exist_ok=True)
            with open(self.temp_dir_path / file_path, "w") as f:
                f.write(file_content)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_files(self) -> None:
        self.assertEqual(
            Directory(
                self.temp_dir_path, {"directory": {"subdir1"}, "file": {"file2"}}
            ).files,
            [
                File(self.temp_dir_path / "file1.txt"),
                File(self.temp_dir_path / "subdir/file3.txt"),
                File(self.temp_dir_path / "subdir/file4.txt"),
                File(self.temp_dir_path / "subdir/file5.txt"),
            ],
        )

    def test_file_paths(self) -> None:
        self.assertEqual(
            Directory(
                self.temp_dir_path, {"directory": {"subdir1"}, "file": {"file2"}}
            ).file_paths,
            [
                self.temp_dir_path / "file1.txt",
                self.temp_dir_path / "subdir/file3.txt",
                self.temp_dir_path / "subdir/file4.txt",
                self.temp_dir_path / "subdir/file5.txt",
            ],
        )

    def test_file_modification_times(self) -> None:
        expected_file_modification_times = {
            file_path: datetime.fromtimestamp(os.path.getmtime(file_path))
            for file_path in [
                self.temp_dir_path / "file1.txt",
                self.temp_dir_path / "subdir/file3.txt",
                self.temp_dir_path / "subdir/file4.txt",
                self.temp_dir_path / "subdir/file5.txt",
            ]
        }

        self.assertEqual(
            Directory(
                self.temp_dir_path, {"directory": {"subdir1"}, "file": {"file2"}}
            ).file_modified_times,
            expected_file_modification_times,
        )

    def test_file_paths_to_content(self) -> None:
        self.assertEqual(
            Directory(
                self.temp_dir_path, {"directory": {"subdir1"}, "file": {"file2"}}
            ).file_paths_to_content,
            {
                str(self.temp_dir_path / "file1.txt"): b"content1",
                str(self.temp_dir_path / "subdir/file3.txt"): b"content3",
                str(self.temp_dir_path / "subdir/file4.txt"): b"content4",
                str(self.temp_dir_path / "subdir/file5.txt"): b"content5",
            },
        )
