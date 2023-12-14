from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
import os

from .file import File
from .string_matcher import StringMatcher


class Directory:
    def __init__(self, path: Path, ignorable_regex_patterns: dict[str, str] = None):
        self._path: Path = path
        self._ignorable_regex_patterns = ignorable_regex_patterns
        self._files: list[File] = self._get_files(self._path)

    def _get_files(self, dir_path: Path) -> list[File]:
        files = []
        for entry_path in os.scandir(dir_path):
            entry_path = Path(entry_path)

            if entry_path.is_file() and not StringMatcher.matches_any_regex_pattern(
                str(entry_path), self._ignorable_regex_patterns["file"]
            ):
                files.append(File(entry_path))

            if entry_path.is_dir() and not StringMatcher.matches_any_regex_pattern(
                str(entry_path), self._ignorable_regex_patterns["directory"]
            ):
                files.extend(self._get_files(entry_path))
        return files

    def get_file_changes(
        self, previous_files: dict[Path, datetime]
    ) -> dict[str, list[tuple[str, bytes]]]:
        previous_file_paths = set(previous_files.keys())
        current_file_paths = set(self.file_paths)

        added_file_paths = list(current_file_paths - previous_file_paths)
        deleted_file_paths = list(previous_file_paths - current_file_paths)
        updated_file_paths = [
            path
            for path in current_file_paths.intersection(previous_file_paths)
            if datetime.fromtimestamp(os.path.getmtime(path)) != previous_files[path]
        ]

        file_path_changes = {
            "add": added_file_paths,
            "update": updated_file_paths,
            "delete": deleted_file_paths,
        }

        with ThreadPoolExecutor() as executor:
            return {
                change: list(executor.map(lambda path: (str(path), File(path).content), paths))
                for change, paths in file_path_changes.items()
            }

    @property
    def files(self) -> list[File]:
        return self._files

    @property
    def file_paths(self) -> list[Path]:
        return [file.path for file in self._files]

    @property
    def file_paths_to_content(self) -> dict[str, bytes]:
        with ThreadPoolExecutor() as executor:
            path_content_pairs = executor.map(
                lambda file: (file.path, file.content), self._files
            )
            return {str(path): content for path, content in path_content_pairs}
