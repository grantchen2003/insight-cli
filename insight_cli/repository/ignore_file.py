from pathlib import Path


class IgnoreFile:
    _NAME = ".insightignore"

    def __init__(self, parent_dir_path: Path):
        self._path = parent_dir_path / IgnoreFile._NAME

    @property
    def is_valid(self) -> bool:
        return self._path.is_file()

    @property
    def names(self) -> set[str]:
        if not self.is_valid:
            return set()

        with open(self._path) as file:
            return set(line.strip() for line in file.read().splitlines())
