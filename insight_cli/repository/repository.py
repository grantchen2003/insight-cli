from pathlib import Path
import time

from insight_cli.api import InitializeRepositoryAPI, ReinitializeRepositoryAPI, QueryRepositoryAPI
from insight_cli.utils import Directory
from .core_dir import CoreDir
from .ignore_file import IgnoreFile


class InvalidRepositoryError(Exception):
    def __init__(self, path: Path):
        self.message = f"{path.resolve()} is not an insight repository"
        super().__init__(self.message)


class Repository:
    class _RepositoryDecorators:
        @staticmethod
        def raise_for_invalid_repository(func):
            def wrapper(self: "Repository", *args, **kwargs):
                if not self.is_valid:
                    raise InvalidRepositoryError(self._path)
                return func(self, *args, **kwargs)

            return wrapper

    def __init__(self, path: Path):
        self._path = path
        self._core_dir = CoreDir(path)
        self._ignore_file = IgnoreFile(path)

    def initialize(self) -> None:
        start = time.perf_counter()
        repository_dir: Directory = Directory(
            self._path, self._ignore_file.regex_patterns
        )
        print(f"dir time: {time.perf_counter() - start}")

        start = time.perf_counter()
        response_data: dict[str, str] = InitializeRepositoryAPI.make_request(
            repository_dir.file_paths_to_content
        )
        print(f"api time: {time.perf_counter() - start}")

        start = time.perf_counter()
        self._core_dir.create(response_data["repository_id"], repository_dir.file_paths)
        print(f"create time: {time.perf_counter() - start}")

    @_RepositoryDecorators.raise_for_invalid_repository
    def reinitialize(self) -> None:
        start = time.perf_counter()
        repository_dir: Directory = Directory(
            self._path, self._ignore_file.regex_patterns
        )
        print(f"dir time: {time.perf_counter() - start}")

        start = time.perf_counter()
        repository_file_changes = repository_dir.get_file_changes(
            previous_files=self._core_dir.path_to_last_updated_times
        )
        print(f"changed files time: {time.perf_counter() - start}")

        start = time.perf_counter()
        ReinitializeRepositoryAPI.make_request(
            self._core_dir.repository_id, repository_file_changes
        )
        print(f"api time: {time.perf_counter() - start}")

        start = time.perf_counter()
        self._core_dir.update(repository_file_changes)
        print(f"core dir time: {time.perf_counter() - start}")

    @_RepositoryDecorators.raise_for_invalid_repository
    def uninitialize(self) -> None:
        self._core_dir.delete()

    @_RepositoryDecorators.raise_for_invalid_repository
    def query(self, query_string: str) -> list[dict]:
        return QueryRepositoryAPI.make_request(
            self._core_dir.repository_id, query_string
        )

    @property
    def is_valid(self) -> bool:
        return self._core_dir.is_valid

    @property
    def path(self) -> Path:
        return self._path
