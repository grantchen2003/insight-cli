from pathlib import Path
import time

from insight_cli.api import (
    InitializeRepositoryAPI,
    ReinitializeRepositoryAPI,
    QueryRepositoryAPI,
)
from insight_cli.utils import Directory, FileChangesDetector
from .core_dir import CoreDir
from .ignore_file import IgnoreFile


class InvalidRepositoryError(Exception):
    def __init__(self, path: Path):
        self.message = f"{path.resolve()} is not an insight repository"
        super().__init__(self.message)


class Repository:
    @staticmethod
    def _raise_for_invalid_repository(func):
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

    @_raise_for_invalid_repository
    def reinitialize(self) -> None:
        total_start = time.perf_counter()
        start = time.perf_counter()
        repository_dir: Directory = Directory(
            self._path, self._ignore_file.regex_patterns
        )
        print(f"dir time: {time.perf_counter() - start}")

        start = time.perf_counter()
        tracked_file_times = self._core_dir.tracked_file_modified_times
        print(f"tracked_file_times time: {time.perf_counter() - start}")

        start = time.perf_counter()
        repo_file_modified_times = repository_dir.file_modified_times
        print(f"repo_file_modified_times time: {time.perf_counter() - start}")

        start = time.perf_counter()
        file_changes_detector = FileChangesDetector(
            previous_file_modified_times=tracked_file_times,
            current_file_modified_times=repo_file_modified_times
        )
        print(f"create detector time: {time.perf_counter() - start}")

        start = time.perf_counter()
        repository_file_changes = file_changes_detector.file_changes
        print(f"file changes time: {time.perf_counter() - start}")

        start = time.perf_counter()
        ReinitializeRepositoryAPI.make_request(
            repository_id=self._core_dir.repository_id,
            repository_file_changes=repository_file_changes
        )
        print(f"api time: {time.perf_counter() - start}")

        start = time.perf_counter()
        repository_file_path_changes = file_changes_detector.file_path_changes
        print(f"file path changes time: {time.perf_counter() - start}")

        start = time.perf_counter()
        self._core_dir.update(repository_file_path_changes)
        print(f"core dir time: {time.perf_counter() - start}")

        print(f"total time: {time.perf_counter() - total_start}")

    @_raise_for_invalid_repository
    def uninitialize(self) -> None:
        self._core_dir.delete()

    @_raise_for_invalid_repository
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
