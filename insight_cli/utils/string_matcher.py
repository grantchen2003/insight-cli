import re


class StringMatcher:
    _cache = {"valid_regex_patterns": set()}

    @classmethod
    def _raise_for_invalid_regex_patterns(cls, patterns: set[str]) -> None:
        patterns = tuple(patterns)

        if patterns in cls._cache["valid_regex_patterns"]:
            return

        for pattern in patterns:
            try:
                re.compile(pattern)
            except re.error as e:
                raise ValueError(f"{pattern} is an invalid regex pattern. {e}")

        cls._cache["valid_regex_patterns"].add(patterns)

    @staticmethod
    def matches_any_regex_pattern(string: str, regex_patterns: set[str]) -> bool:
        StringMatcher._raise_for_invalid_regex_patterns(regex_patterns)

        return any(re.search(regex_pattern, string) for regex_pattern in regex_patterns)
