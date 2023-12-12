from pathlib import Path


class IgnoreFile:
    _NAME = ".insightignore"

    def __init__(self, parent_dir_path: Path):
        self._path = parent_dir_path / IgnoreFile._NAME

    @property
    def regex_patterns(self) -> dict[str, set]:
        scope_to_regex_patterns = {"directory": set(), "file": set()}

        if not self._path.is_file():
            return scope_to_regex_patterns

        active_scopes = list(scope_to_regex_patterns.keys())

        with open(self._path) as file:
            for line in file.read().splitlines():
                line = line.strip()

                if line == "":
                    continue

                line_is_directory_scope_comment = line == "## _directory_"
                if line_is_directory_scope_comment:
                    active_scopes = ["directory"]
                    continue

                line_is_file_scope_comment = line == "## _file_"
                if line_is_file_scope_comment:
                    active_scopes = ["file"]
                    continue

                line_is_comment = line.startswith("#")
                if line_is_comment:
                    continue

                if line.startswith(r"\#"):
                    line = line[1::]

                for scope in active_scopes:
                    scope_to_regex_patterns[scope].add(line)

        return scope_to_regex_patterns
