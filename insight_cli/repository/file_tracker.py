from datetime import datetime
from pathlib import Path
import json, os


class FileTracker:
    _FILE_NAME = "file_tracker.json"

    def __init__(self, parent_dir_file_path: Path):
        self._file_path: Path = parent_dir_file_path / FileTracker._FILE_NAME
        self._data: dict[str, float] = self._read_from_file()

    def _write_to_file(self) -> None:
        with open(self._file_path, "w") as file:
            file.write(json.dumps(self._data, indent=4))

    def _read_from_file(self) -> dict[str, float]:
        if not self._file_path.is_file():
            return {}
        with open(self._file_path, "r") as file:
            return json.load(file)

    def _add(self, file_paths: list[Path]) -> None:
        for file_path in file_paths:
            if not file_path.is_file():
                raise FileNotFoundError(f"cannot find file at {file_path}")
            if str(file_path) in self._data:
                raise ValueError(
                    f"cannot add file path that already exists: {file_path}"
                )
            self._data[str(file_path)] = os.path.getmtime(file_path)

    def _update(self, file_paths: list[Path]) -> None:
        for file_path in file_paths:
            if not file_path.is_file():
                raise FileNotFoundError(f"cannot find file at {file_path}")
            if str(file_path) not in self._data:
                raise ValueError(
                    f"cannot update file path that does not exist: {file_path}"
                )
            self._data[str(file_path)] = os.path.getmtime(file_path)

    def _delete(self, file_paths: list[Path]) -> None:
        for file_path in file_paths:
            if str(file_path) not in self._data:
                raise ValueError(
                    f"cannot delete file path that does not exist: {file_path}"
                )
            del self._data[str(file_path)]

    def create(self, file_paths: list[Path]) -> None:
        self._add(file_paths)
        self._write_to_file()

    def change_file_paths(
        self,
        paths_to_add: list[Path],
        paths_to_update: list[Path],
        paths_to_delete: list[Path],
    ) -> None:
        self._add(paths_to_add)
        self._update(paths_to_update)
        self._delete(paths_to_delete)
        self._write_to_file()

    @property
    def tracked_file_modified_times(self) -> dict[Path, datetime]:
        return {
            Path(file_path): datetime.fromtimestamp(last_updated_time)
            for file_path, last_updated_time in self._data.items()
        }
