from pathlib import Path


class File:
    def __init__(self, path: Path):
        self._path: Path = path
        self._content: bytes = File._get_content(path)

    @staticmethod
    def _get_content(file_path: Path) -> bytes:
        with open(file_path, "rb") as file:
            return file.read()

    @property
    def path(self) -> Path:
        return self._path

    @property
    def content(self) -> bytes:
        return self._content
