import re


class StringMatcher:
    _cache = {"_raise_for_invalid_regex_patterns": {}}

    @classmethod
    def _raise_for_invalid_regex_patterns(cls, patterns: list[str]) -> None:
        cache = cls._cache["_raise_for_invalid_regex_patterns"]
        patterns = tuple(patterns)

        if patterns not in cache:
            cache[patterns] = None

            for pattern in patterns:
                try:
                    re.compile(pattern)
                except re.error as e:
                    cache[patterns] = ValueError(
                        f"{pattern} is an invalid regex pattern. {e}"
                    )

        if cache[patterns]:
            raise cache[patterns]

    @staticmethod
    def matches_any_regex_pattern(query_string: str, regex_patterns: list[str]) -> bool:
        StringMatcher._raise_for_invalid_regex_patterns(regex_patterns)
        return any(
            re.match(regex_pattern, query_string) for regex_pattern in regex_patterns
        )
