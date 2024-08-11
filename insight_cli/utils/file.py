from pathlib import Path
import functools, os


class File:
    _instances: dict[Path, "File"] = {}

    def __new__(cls, path: Path):
        """
        The __new__ method ensures a Singleton pattern per unique
        path. If an instance A is created with a path used by
        another instance B, A is not a new instance but is B itself.
        """
        if path not in cls._instances:
            cls._instances[path] = super(File, cls).__new__(cls)

        return cls._instances[path]

    def __init__(self, path: Path):
        self._path: Path = path

    @property
    def path(self) -> Path:
        return self._path

    @property
    def size_bytes(self) -> int:
        return os.path.getsize(self._path)

    @property
    @functools.lru_cache(maxsize=None)
    def content(self) -> bytes:
        if not self._path.is_file():
            return b""

        with open(self._path, "rb") as file:
            return file.read()
