from datetime import datetime
from pathlib import Path
import json, os


class UpdatesFile:
    _NAME = "updates.json"

    def __init__(self, parent_dir_path: Path):
        self._path: Path = parent_dir_path / UpdatesFile._NAME
        self._data: dict[str, float] = self._read_from_updates_file()

    def _write_to_updates_file(self) -> None:
        with open(self._path, "w") as file:
            file.write(json.dumps(self._data, indent=4))

    def _read_from_updates_file(self) -> dict[str, float]:
        if not self._path.is_file():
            return {}
        with open(self._path, "r") as file:
            return json.load(file)

    def _add(self, paths: list[Path]) -> None:
        for path in paths:
            if str(path) in self._data:
                raise ValueError(f"{path} is already exists")
            self._data[str(path)] = os.path.getmtime(path)

    def _update(self, paths: list[Path]) -> None:
        for path in paths:
            if str(path) not in self._data:
                raise ValueError(f"{path} does not exists")
            self._data[str(path)] = os.path.getmtime(path)

    def _delete(self, paths: list[Path]) -> None:
        for path in paths:
            if str(path) not in self._data:
                raise ValueError(f"{path} does not exists")
            del self._data[str(path)]

    def create(self, paths: list[Path]) -> None:
        self._data = {str(path): os.path.getmtime(path) for path in paths}
        self._write_to_updates_file()

    def reinitialize(
            self,
            paths_to_add: list[Path],
            paths_to_update: list[Path],
            paths_to_delete: list[Path]
    ) -> None:
        self._add(paths_to_add)
        self._update(paths_to_update)
        self._delete(paths_to_delete)
        self._write_to_updates_file()

    @property
    def data(self) -> dict[Path, datetime]:
        return {
            Path(file_path): datetime.fromtimestamp(last_updated)
            for file_path, last_updated in self._data.items()
        }
