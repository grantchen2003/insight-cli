from pathlib import Path


class InvalidDotInsightignoreFilePathError(Exception):
    def __init__(self, dir_path: Path):
        self.message = f"{dir_path} is an invalid .insightignore file path"
        super().__init__(self.message)


def _exists(dot_insightignore_file_path: Path) -> bool:
    return dot_insightignore_file_path.is_file()


def get_file_name() -> str:
    return ".insightignore"


def get_ignorable_names(dot_insightignore_file_path: Path) -> set[str]:
    if not _exists(dot_insightignore_file_path):
        return set()

    with open(dot_insightignore_file_path) as dot_insightignore_file:
        return set(line.strip() for line in dot_insightignore_file.read().splitlines())
