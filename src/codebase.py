import insight_dir
import insightignore_file
from pathlib import Path
from utils import directory as DirectoryUtils, api_requests as ApiRequestUtils


def initialize(codebase_dir_path: Path) -> None:
    insight_dir_path: Path = codebase_dir_path / "insight"

    # if a valid .insight directory exists, reinitialize the codebase
    if insight_dir.is_valid(insight_dir_path):
        reinitialize(codebase_dir_path)
        return

    # read .insightignore file
    insightignore_file_path: Path = codebase_dir_path / ".insightignore"
    ignorable_names: list[str] = insightignore_file.get_ignorable_names(
        insightignore_file_path
    )

    # get all dirs/files in codebase excluding those in .insightignore
    codebase_dir: DirectoryUtils.Directory = DirectoryUtils.create_directory_from_path(
        dir_path=codebase_dir_path, ignorable_names=ignorable_names
    )

    # send codebase to api which responds with codebase_id
    response_data: dict[str, str] = ApiRequestUtils.initialize_codebase(codebase_dir)
    codebase_id: str = response_data["codebase_id"]

    # create .insight directory
    insight_dir.create(codebase_id)


def reinitialize(codebase_dir_path: Path) -> None:
    insight_dir_path: Path = codebase_dir_path / "insight"

    # raises Exception if [insight_dir_path] is an invalid .insight dir path
    if not insight_dir.is_valid(insight_dir_path):
        raise insight_dir.InvalidInsightDirectoryPathError(insight_dir_path)
    # TODO


def uninitialize(codebase_dir_path: Path) -> None:
    print("uninitialize")
    # TODO
