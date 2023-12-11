from datetime import datetime
from pathlib import Path
import json, os


class UpdatesFile:
    _NAME = "updates.json"

    def __init__(self, parent_dir_path: Path):
        self._path = parent_dir_path / UpdatesFile._NAME

    @staticmethod
    def _get_last_updated_timestamps(paths: list[Path]) -> dict[str, float]:
        return {str(path): os.path.getmtime(path) for path in paths}

    def create(self, paths: list[Path]) -> None:
        paths_to_last_updated: dict[
            str, float
        ] = UpdatesFile._get_last_updated_timestamps(paths)

        with open(self._path, "w") as file:
            content = json.dumps(paths_to_last_updated, indent=4)
            file.write(content)

    def add(self, paths: list[Path]) -> None:
        existing_data: dict[str, float] = self._get_raw_data()

        new_data = existing_data

        for path in paths:
            if str(path) in existing_data:
                raise ValueError(f"{path} is already exists")
            new_data[path] = paths[path]

        with open(self._path, "w") as file:
            content = json.dumps(new_data, indent=4)
            file.write(content)

    def update(self, paths: list[Path]) -> None:
        existing_data: dict[str, float] = self._get_raw_data()

        new_data = existing_data

        for path in paths:
            if str(path) not in existing_data:
                raise ValueError(f"{path} does not exists")
            new_data[path] = paths[path]

        with open(self._path, "w") as file:
            content = json.dumps(new_data, indent=4)
            file.write(content)

    def delete(self, paths: list[Path]) -> None:
        existing_data: dict[str, float] = self._get_raw_data()

        new_data = existing_data

        for path in paths:
            if str(path) not in existing_data:
                raise ValueError(f"{path} does not exists")
            del new_data[path]

        with open(self._path, "w") as file:
            content = json.dumps(new_data, indent=4)
            file.write(content)

    def _get_raw_data(self) -> dict[str, float]:
        with open(self._path, "r") as file:
            return json.load(file)

    @property
    def data(self) -> dict[Path, datetime]:
        return {
            Path(file_path): datetime.fromtimestamp(last_updated)
            for file_path, last_updated in self._get_raw_data().items()
        }
