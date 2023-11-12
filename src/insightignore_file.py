from pathlib import Path


class InvalidInsightignoreFilePathError(Exception):
    def __init__(self, dir_path: Path):
        self.message = f"{dir_path} is an invalid .insightignore file path"
        super().__init__(self.message)


def exists(insightignore_file_path: Path) -> bool:
    return insightignore_file_path.is_file()


def get_lines(insightignore_file_path: Path) -> set[str]:
    if not exists(insightignore_file_path):
        raise InvalidInsightignoreFilePathError(insightignore_file_path)

    with open(insightignore_file_path) as insightignore_file:
        insightignore_file_lines = insightignore_file.read().splitlines()

    return set(line.strip() for line in insightignore_file_lines)


def get_ignorable_names(insightignore_file_path: Path) -> set[str]:
    ignorable_names = set()
    if exists(insightignore_file_path):
        ignorable_names = get_lines(insightignore_file_path)
    return ignorable_names
