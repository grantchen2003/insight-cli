from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
import os

from .file import File
from .string_matcher import StringMatcher


class Directory:
    def __init__(
        self,
        path: Path,
        ignorable_regex_patterns: dict[str, set],
        allowed_file_extensions: set[str],
    ):
        self._path: Path = path
        self._ignorable_regex_patterns = ignorable_regex_patterns
        self._allowed_file_extensions = allowed_file_extensions
        self._files: list[File] = self._get_files(self._path)

    def _entry_path_is_ignorable(self, entry_path: Path, pattern_scope: str) -> bool:
        if pattern_scope == "file":
            _, file_extension = os.path.splitext(entry_path)
            if file_extension not in self._allowed_file_extensions:
                return True

        return StringMatcher.matches_any_regex_pattern(
            str(entry_path), self._ignorable_regex_patterns[pattern_scope]
        )

    def _get_files(self, dir_path: Path) -> list[File]:
        files = []

        for root, directories, file_names in os.walk(dir_path):
            root_path = Path(root)

            directories[:] = [
                directory
                for directory in directories
                if not self._entry_path_is_ignorable(root_path / directory, "directory")
            ]

            for file_name in file_names:
                file_path = root_path / file_name
                if not self._entry_path_is_ignorable(file_path, "file"):
                    files.append(File(file_path))

        return files

    @property
    def files(self) -> list[File]:
        return self._files

    @property
    def file_paths(self) -> list[Path]:
        return [file.path for file in self._files]

    @property
    def file_modified_times(self) -> dict[Path, datetime]:
        return {
            file_path: datetime.fromtimestamp(os.path.getmtime(file_path))
            for file_path in self.file_paths
        }

    @property
    def file_paths_to_content(self) -> dict[str, bytes]:
        with ThreadPoolExecutor() as executor:
            path_content_pairs = executor.map(
                lambda file: (file.path, file.content), self._files
            )
            return {str(path): content for path, content in path_content_pairs}

    @property
    def is_empty(self) -> bool:
        return len(self._files) == 0
    
    @property
    def largest_file_by_size(self) -> File | None:
        if self.is_empty:
            return None
        
        return max(self._files, key=lambda file: os.path.getsize(file.path))
