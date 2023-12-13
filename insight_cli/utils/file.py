from pathlib import Path
import functools


class File:
    def __init__(self, path: Path):
        self._path: Path = path

    @property
    def path(self) -> Path:
        return self._path

    @property
    @functools.lru_cache(maxsize=None)
    def content(self) -> bytes:
        with open(self._path, "rb") as file:
            return file.read()
