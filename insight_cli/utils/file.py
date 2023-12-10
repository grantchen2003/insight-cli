from io import BufferedReader
from pathlib import Path
import os


class File:
    def __init__(self, path: Path, binary_data: BufferedReader):
        self._path: Path = path
        self._binary_data: BufferedReader = binary_data

    @staticmethod
    def create_in_file_system(file: "File") -> None:
        with open(file.path, "w") as f:
            f.write(file.binary_data)

    @staticmethod
    def create_from_path(file_path: Path) -> "File":
        with open(file_path, 'rb') as binary_file:
            return File(path=file_path, binary_data=binary_file.read())

    @property
    def path(self) -> Path:
        return self._path

    @property
    def binary_data(self) -> BufferedReader:
        return self._binary_data

    @property
    def size_bytes(self) -> int:
        return os.path.getsize(self.path)
