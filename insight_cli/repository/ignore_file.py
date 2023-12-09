from pathlib import Path


class IgnoreFile:
    _NAME = ".insightignore"

    def __init__(self, parent_dir_path: Path):
        self._path = parent_dir_path / IgnoreFile._NAME

    @property
    def is_valid(self) -> bool:
        return self._path.is_file()

    @property
    def regex_patterns(self) -> dict[str, set]:
        scope_to_regex_patterns = {"directory": set(), "file": set()}

        if not self.is_valid:
            return scope_to_regex_patterns

        active_pattern_scopes = list(scope_to_regex_patterns.keys())

        with open(self._path) as file:
            for line in file.read().splitlines():
                line = line.strip()

                if line == "":
                    continue

                elif line == "## _directory_":
                    active_pattern_scopes = ["directory"]
                    continue

                elif line == "## _file_":
                    active_pattern_scopes = ["file"]
                    continue

                elif line.startswith("#"):
                    continue

                if line.startswith(r"\#"):
                    line = line[1::]

                for pattern_scope in active_pattern_scopes:
                    scope_to_regex_patterns[pattern_scope].add(line)

        return scope_to_regex_patterns
