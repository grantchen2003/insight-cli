from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from datetime import datetime
import os

from .file import File
from .string_matcher import StringMatcher


class Directory:
    def __init__(self, path: Path, ignorable_regex_patterns: dict[str, str] = None):
        self._path: Path = path
        self._ignorable_regex_patterns = ignorable_regex_patterns
        self._files: list[File] = []
        self._populate_with_files_in_dir(self._path)

    def _populate_with_files_in_dir(self, dir_path: Path) -> None:
        for entry_path in os.scandir(dir_path):
            entry_path = Path(entry_path)

            if entry_path.is_file() and not StringMatcher.matches_any_regex_pattern(
                str(entry_path), self._ignorable_regex_patterns["file"]
            ):
                self._add_file(File(entry_path))

            if entry_path.is_dir() and not StringMatcher.matches_any_regex_pattern(
                str(entry_path), self._ignorable_regex_patterns["directory"]
            ):
                self._populate_with_files_in_dir(entry_path)

    def _add_file(self, file: File) -> None:
        self._files.append(file)

    @property
    def path(self) -> Path:
        return self._path

    @property
    def files(self) -> list[File]:
        return self._files

    @property
    def nested_file_paths(self) -> list[Path]:
        return [file.path for file in self._files]

    @property
    def files_path_to_content(self) -> dict[str:bytes]:
        def process_file(file: File) -> tuple[Path, bytes]:
            return file.path, file.content

        with ThreadPoolExecutor() as executor:
            return {
                str(path): content
                for path, content in executor.map(process_file, self._files)
            }
