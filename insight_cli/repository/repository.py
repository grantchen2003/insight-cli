from pathlib import Path

from insight_cli.api import API
from insight_cli.utils import Directory
from .core_dir import CoreDir
from .ignore_file import IgnoreFile


class InvalidRepositoryError(Exception):
    def __init__(self, path):
        self.message = f"{Path(path).resolve()} is an invalid insight repository."
        super().__init__(self.message)


class Repository:
    def _raise_for_invalid_repository(func):
        def wrapper(self: "Repository", *args, **kwargs):
            if not self.is_valid:
                raise InvalidRepositoryError(self._path)

            return func(*args, **kwargs)

        return wrapper

    def __init__(self, path: Path):
        self._path = path
        self._core_dir = CoreDir(path)
        self._ignore_file = IgnoreFile(path)

    def initialize(self) -> None:
        repository: Directory = Directory.create_from_path(
            dir_path=self._path, ignorable_names=self._ignore_file.names
        )

        response_data: dict[str, str] = API.make_initialize_repository_request(
            repository
        )

        repository_id: str = response_data["repository_id"]

        self._core_dir.create(repository_id)

    @_raise_for_invalid_repository
    def reinitialize(self) -> None:
        repository_dir: Directory = Directory.create_from_path(
            dir_path=self._path, ignorable_names=self._ignore_file.names
        )

        API.make_reinitialize_repository_request(
            repository_dir, self._core_dir.repository_id
        )

    @_raise_for_invalid_repository
    def uninitialize(self) -> None:
        self._core_dir.delete()

    @_raise_for_invalid_repository
    def query(self, query_string: str) -> list[dict]:
        return API.make_query_repository_request(
            self._core_dir.repository_id, query_string
        )

    @property
    def is_valid(self) -> bool:
        return self._core_dir.is_valid
