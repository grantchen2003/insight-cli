from pathlib import Path

from insight_cli.api import (
    InitializeRepositoryAPI,
    QueryRepositoryAPI,
    ReinitializeRepositoryAPI,
    UninitializeRepositoryAPI,
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
        repository_dir: Directory = Directory(
            self._path, self._ignore_file.regex_patterns
        )

        response_data: dict[str, str] = InitializeRepositoryAPI.make_request(
            repository_dir.file_paths_to_content
        )

        self._core_dir.create(response_data["repository_id"], repository_dir.file_paths)

    @_raise_for_invalid_repository
    def reinitialize(self) -> None:
        repository_dir: Directory = Directory(
            self._path, self._ignore_file.regex_patterns
        )

        file_changes_detector = FileChangesDetector(
            previous_file_modified_times=self._core_dir.tracked_file_modified_times,
            current_file_modified_times=repository_dir.file_modified_times,
        )

        if file_changes_detector.no_files_changes_exist:
            return

        ReinitializeRepositoryAPI.make_request(
            repository_id=self._core_dir.repository_id,
            repository_file_changes=file_changes_detector.file_changes,
        )

        self._core_dir.update(file_changes_detector.file_path_changes)

    @_raise_for_invalid_repository
    def uninitialize(self) -> None:
        UninitializeRepositoryAPI.make_request(self._core_dir.repository_id)
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
