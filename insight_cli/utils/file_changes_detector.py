from datetime import datetime
from pathlib import Path
import concurrent, functools

from .file import File


class FileChangesDetector:
    @staticmethod
    def _get_file_content(change, path) -> tuple[str, bytes]:
        match change:
            case "add":
                content = File(path).content
            case "update":
                content = File(path).content
            case "delete":
                content = b""
            case _:
                raise ValueError(f"Invalid change: {change}")

        return str(path), content

    def __init__(
        self,
        previous_file_modified_times: dict[Path, datetime],
        current_file_modified_times: dict[Path, datetime],
    ):
        """
        Initializes with immutable dictionaries for file paths and
        modification times. Once provided, these dictionaries remain
        unmodifiable to facilitate caching in the file_path_changes
        mechanism.
        """
        self._previous_file_modified_times: dict[
            Path, datetime
        ] = previous_file_modified_times
        self._current_file_modified_times: dict[
            Path, datetime
        ] = current_file_modified_times

    @property
    def _current_file_paths(self) -> set[Path]:
        return set(self._current_file_modified_times.keys())

    @property
    def _previous_file_paths(self) -> set[Path]:
        return set(self._previous_file_modified_times.keys())

    @property
    def _added_files(self) -> list[Path]:
        return list(self._current_file_paths - self._previous_file_paths)

    @property
    def _deleted_files(self) -> list[Path]:
        return list(self._previous_file_paths - self._current_file_paths)

    @property
    def _updated_files(self) -> list[Path]:
        return [
            path
            for path in self._current_file_paths & self._previous_file_paths
            if self._current_file_modified_times[path]
            != self._previous_file_modified_times[path]
        ]

    @property
    @functools.lru_cache(maxsize=1)
    def file_path_changes(self) -> dict[str, list[Path]]:
        return {
            "add": self._added_files,
            "update": self._updated_files,
            "delete": self._deleted_files,
        }

    @property
    def file_changes(self) -> dict[str, list[tuple[str, bytes]]]:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            return {
                change: list(
                    executor.map(
                        FileChangesDetector._get_file_content,
                        [change] * len(paths),
                        paths,
                    )
                )
                for change, paths in self.file_path_changes.items()
            }

    @property
    def no_files_changes_exist(self) -> bool:
        return all(
            not changed_file_paths
            for changed_file_paths in self.file_path_changes.values()
        )
