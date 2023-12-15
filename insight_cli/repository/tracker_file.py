from datetime import datetime
from pathlib import Path
import json, os


class TrackerFile:
    _NAME = "tracker.json"

    def __init__(self, parent_dir_path: Path):
        self._path: Path = parent_dir_path / TrackerFile._NAME
        self._data: dict[str, float] = self._read_from_file()

    def _write_to_file(self) -> None:
        with open(self._path, "w") as file:
            file.write(json.dumps(self._data, indent=4))

    def _read_from_file(self) -> dict[str, float]:
        if not self._path.is_file():
            return {}
        with open(self._path, "r") as file:
            return json.load(file)

    def _add(self, paths: list[Path]) -> None:
        for path in paths:
            if str(path) in self._data:
                raise ValueError(
                    f"cannot add path that already exists: {path}"
                )
            self._data[str(path)] = os.path.getmtime(path)

    def _update(self, paths: list[Path]) -> None:
        for path in paths:
            if str(path) not in self._data:
                raise ValueError(
                    f"cannot update path that does not exist: {path}"
                )
            self._data[str(path)] = os.path.getmtime(path)

    def _delete(self, paths: list[Path]) -> None:
        for path in paths:
            if str(path) not in self._data:
                raise ValueError(
                    f"cannot delete path that does not exist: {path}"
                )
            del self._data[str(path)]

    def create(self, paths: list[Path]) -> None:
        self._add(paths)
        self._write_to_file()

    def change_paths(
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
            Path(path): datetime.fromtimestamp(last_updated_time)
            for path, last_updated_time in self._data.items()
        }
