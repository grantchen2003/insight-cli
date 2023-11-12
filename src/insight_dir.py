from pathlib import Path


class InvalidInsightDirectoryPathError(Exception):
    def __init__(self, dir_path: Path):
        self.message = f"{dir_path} is an invalid .insight dir path"
        super().__init__(self.message)


def is_valid(insight_dir_path: Path) -> bool:
    # TODO, check it has the right files and the files have the right content
    return insight_dir_path.is_dir()


def create(codebase_id: str) -> None:
    # TODO
    pass
