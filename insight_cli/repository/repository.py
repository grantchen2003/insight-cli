from pathlib import Path
import time

from insight_cli.api import API
from insight_cli.utils import Directory, File
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
        repository_dir: Directory = Directory.create_from_path(
            dir_path=self._path,
            ignorable_regex_patterns=self._ignore_file.regex_patterns,
        )
        print(f"dir time: {time.perf_counter() - start}")

        start = time.perf_counter()
        response_data: dict[str, str] = API.make_initialize_repository_request(
            repository_dir.nested_files_path_to_bytes
        )
        print(f"api time: {time.perf_counter() - start}")

        repository_id: str = response_data["repository_id"]

        start = time.perf_counter()
        self._core_dir.create(repository_id, repository_dir.nested_file_paths)
        print(f"create time: {time.perf_counter() - start}")

    @_RepositoryDecorators.raise_for_invalid_repository
    def reinitialize(self) -> None:
        start = time.perf_counter()
        repository_dir = Directory.create_from_path(
            dir_path=self._path,
            ignorable_regex_patterns=self._ignore_file.regex_patterns,
        )
        print(f"dir time: {time.perf_counter() - start}")

        start = time.perf_counter()
        file_paths_to_reinitialize: dict[
            str, list[Path]
        ] = repository_dir.compare_file_paths(self._core_dir.files_path_to_last_updated)
        print(f"compare time: {time.perf_counter() - start}")

        start = time.perf_counter()
        API.make_reinitialize_repository_request(
            file_paths_to_reinitialize,
            self._core_dir.repository_id,
        )
        print(f"api time: {time.perf_counter() - start}")

        start = time.perf_counter()
        self._core_dir.reinitialize(file_paths_to_reinitialize)
        print(f"local reinit time: {time.perf_counter() - start}")

    @_RepositoryDecorators.raise_for_invalid_repository
    def uninitialize(self) -> None:
        self._core_dir.delete()

    @_RepositoryDecorators.raise_for_invalid_repository
    def query(self, query_string: str) -> list[dict]:
        return API.make_query_repository_request(
            self._core_dir.repository_id, query_string
        )

    @property
    def is_valid(self) -> bool:
        return self._core_dir.is_valid

    @property
    def path(self) -> Path:
        return self._path
