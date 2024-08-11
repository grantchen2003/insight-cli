from pathlib import Path

from insight_cli.api import (
    CreateRepositoryAPI,
    InitializeRepositoryAPI,
    QueryRepositoryAPI,
    ReinitializeRepositoryAPI,
    UninitializeRepositoryAPI,
)
from insight_cli.utils import Directory, File, FileChangesDetector
from .manager import Manager
from .pattern_ignorer import PatternIgnorer


class InvalidRepositoryError(Exception):
    def __init__(self, path: Path):
        self.message = f"{path.resolve()} is not an insight repository"
        super().__init__(self.message)


class FileSizeExceededError(Exception):
    def __init__(self, file: File, max_allowed_file_size_bytes: int):
        def bytes_to_mb(size_bytes):
            return size_bytes / (1024 * 1024)

        self.message = f"{file.path} has a size of {bytes_to_mb(file.size_bytes):.2f}MB which exceeds the max allowed file size of {bytes_to_mb(max_allowed_file_size_bytes):.2f}MB"
        super().__init__(self.message)


class Repository:
    def __init__(self, path: Path):
        self._ALLOWED_FILE_EXTENSIONS = {".py"}
        self._MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024  # 10MB
        self._path = path
        self._manager = Manager(path)
        self._pattern_ignorer = PatternIgnorer(path)
        self._is_valid = self._manager.is_valid

    @property
    def _id(self) -> str:
        return self._manager.repository_id

    @property
    def is_valid(self) -> bool:
        return self._is_valid

    @property
    def path(self) -> Path:
        return self._path

    def _raise_for_invalid_repository(self) -> None:
        if not self.is_valid:
            raise InvalidRepositoryError(self._path)

    def _raise_for_file_size_exceeded(self, file: File) -> None:
        if file.size_bytes > self._MAX_FILE_SIZE_BYTES:
            raise FileSizeExceededError(file, self._MAX_FILE_SIZE_BYTES)

    def initialize(self) -> None:
        repository_dir: Directory = Directory(
            path=self._path,
            ignorable_regex_patterns=self._pattern_ignorer.regex_patterns,
            allowed_file_extensions=self._ALLOWED_FILE_EXTENSIONS,
        )
        
        self._raise_for_file_size_exceeded(repository_dir.largest_file_by_size)

        response_data = CreateRepositoryAPI.make_request()

        InitializeRepositoryAPI.make_request(
            response_data["repository_id"], repository_dir.file_paths_to_content
        )

        self._manager.create(response_data["repository_id"], repository_dir.file_paths)

        self._is_valid = True

    def reinitialize(self) -> None:
        self._raise_for_invalid_repository()

        repository_dir: Directory = Directory(
            path=self._path,
            ignorable_regex_patterns=self._pattern_ignorer.regex_patterns,
            allowed_file_extensions=self._ALLOWED_FILE_EXTENSIONS,
        )
        
        self._raise_for_file_size_exceeded(repository_dir.largest_file_by_size)

        file_changes_detector = FileChangesDetector(
            previous_file_modified_times=self._manager.tracked_file_modified_times,
            current_file_modified_times=repository_dir.file_modified_times,
        )

        if file_changes_detector.no_files_changes_exist:
            return

        ReinitializeRepositoryAPI.make_request(
            repository_id=self._id,
            repository_file_changes=file_changes_detector.file_changes,
        )

        self._manager.update(file_changes_detector.file_path_changes)

        self._is_valid = True

    def uninitialize(self) -> None:
        self._raise_for_invalid_repository()

        UninitializeRepositoryAPI.make_request(self._id)

        self._manager.delete()

        self._is_valid = False

    def query(self, query_string: str, limit: int) -> list[dict] | None:
        self._raise_for_invalid_repository()

        self.reinitialize()

        return QueryRepositoryAPI.make_request(self._id, query_string, limit)
