from pathlib import Path

from . import dot_insight_dir
from . import dot_insightignore_file
from .. import utils
from .api import (
    make_initialize_repository_request,
    make_reinitialize_repository_request,
)
from ..utils.directory import Directory


def initialize(repository_dir_path: Path) -> None:
    dot_insight_dir_path: Path = repository_dir_path / dot_insight_dir.get_dir_name()

    if dot_insight_dir.is_valid(dot_insight_dir_path):
        reinitialize(repository_dir_path)
        return

    dot_insightignore_file_path: Path = (
        repository_dir_path / dot_insightignore_file.get_file_name()
    )

    ignorable_names: list[str] = dot_insightignore_file.get_ignorable_names(
        dot_insightignore_file_path
    )

    repository: Directory = utils.Directory.create_from_path(
        dir_path=repository_dir_path, ignorable_names=ignorable_names
    )

    response_data: dict[str, str] = make_initialize_repository_request(repository)

    repository_id: str = response_data["repository_id"]

    dot_insight_dir.create(dot_insight_dir_path, repository_id)


def reinitialize(repository_dir_path: Path) -> None:
    dot_insight_dir_path: Path = repository_dir_path / dot_insight_dir.get_dir_name()

    if not dot_insight_dir.is_valid(dot_insight_dir_path):
        raise dot_insight_dir.InvalidDotInsightDirectoryPathError(dot_insight_dir_path)

    dot_insightignore_file_path: Path = (
        repository_dir_path / dot_insightignore_file.get_file_name()
    )

    ignorable_names: list[str] = dot_insightignore_file.get_ignorable_names(
        dot_insightignore_file_path
    )

    repository_dir: Directory = utils.Directory.create_from_path(
        dir_path=repository_dir_path, ignorable_names=ignorable_names
    )

    repository_id: str = dot_insight_dir.get_repository_id(dot_insight_dir_path)

    make_reinitialize_repository_request(repository_dir, repository_id)


def uninitialize(repository_dir_path: Path) -> None:
    dot_insight_dir_path: Path = repository_dir_path / dot_insight_dir.get_dir_name()

    dot_insight_dir.delete(dot_insight_dir_path)
