from pathlib import Path

from insight_cli.repository.core_dir import CoreDir
from insight_cli.repository.ignore_file import IgnoreFile
from insight_cli.api import API
from insight_cli.utils import Directory


class Repository:
    def __init__(self, path: Path):
        self._path = path
        self._core_dir = CoreDir(path)
        self._ignore_file = IgnoreFile(path)

    def initialize(self) -> None:
        repository: Directory = Directory.create_from_path(
            dir_path=self._path, ignorable_names=self._ignore_file.names
        )

        response_data: dict[str, str] = API.make_initialize_repository_request(
            repository
        )

        repository_id: str = response_data["repository_id"]

        self._core_dir.create(repository_id)

    def reinitialize(self) -> None:
        repository_dir: Directory = Directory.create_from_path(
            dir_path=self._path, ignorable_names=self._ignore_file.names
        )

        API.make_reinitialize_repository_request(
            repository_dir, self._core_dir.repository_id
        )

    def uninitialize(self) -> None:
        self._core_dir.delete()

    def query(self, query_string: str):
        return API.make_query_repository_request(
            self._core_dir.repository_id, query_string
        )

    @property
    def is_valid(self) -> bool:
        return self._core_dir.is_valid
