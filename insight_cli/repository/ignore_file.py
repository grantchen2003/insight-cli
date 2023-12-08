from pathlib import Path


class IgnoreFile:
    _NAME = ".insightignore"

    def __init__(self, parent_dir_path: Path):
        self._path = parent_dir_path / IgnoreFile._NAME

    @property
    def is_valid(self) -> bool:
        return self._path.is_file()

    @property
    def regex_patterns(self) -> list[str]:
        if not self.is_valid:
            return []

        with open(self._path) as file:
            return [line.strip() for line in file.read().splitlines() if line.strip() != ""]
