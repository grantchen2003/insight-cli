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

        regex_patterns = set()
        with open(self._path) as file:
            for line in file.read().splitlines():
                line = line.strip()

                line_is_empty = line == ""
                line_is_a_comment = line.startswith("#")

                if line_is_empty or line_is_a_comment:
                    continue

                if line.startswith("\#"):
                    line = line[1::]

                regex_patterns.add(line)

        return list(regex_patterns)
