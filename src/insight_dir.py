from pathlib import Path


class InvalidInsightDirectoryPathError(Exception):
    def __init__(self, dir_path: Path):
        self.message = f"{dir_path} is an invalid .insight dir path"
        super().__init__(self.message)


def exists(insight_dir_path: Path) -> bool:
    return insight_dir_path.is_dir()


def is_valid(insight_dir_path: Path) -> bool:
    return exists(insight_dir_path)
