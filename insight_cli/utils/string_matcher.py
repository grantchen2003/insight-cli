import functools, re


class StringMatcher:
    @staticmethod
    def _convert_list_args_to_tuple(func):
        def wrapper(*args, **kwargs):
            args = [tuple(x) if isinstance(x, list) else x for x in args]
            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    @_convert_list_args_to_tuple
    @functools.lru_cache(maxsize=None)
    def _raise_for_invalid_regex_patterns(patterns: list[str]) -> None:
        for pattern in patterns:
            try:
                re.compile(pattern)
            except re.error as e:
                raise ValueError(f"{pattern} is an invalid regex pattern. {e}")

    @staticmethod
    def matches_any_regex_pattern(query_string: str, regex_patterns: list[str]) -> bool:
        StringMatcher._raise_for_invalid_regex_patterns(regex_patterns)
        return any(
            re.match(regex_pattern, query_string) for regex_pattern in regex_patterns
        )
