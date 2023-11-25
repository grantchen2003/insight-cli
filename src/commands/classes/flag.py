class Flag:
    @staticmethod
    def _raise_for_invalid_flag(string: str):
        if not isinstance(string, str):
            raise TypeError("flag must be a str")

        if string.strip() != string or string == "" or string[0] != "-":
            raise ValueError("string is not in a flag format")

    def __init__(self, string: str):
        Flag._raise_for_invalid_flag(string)
        self._suffix = string.lstrip("-")
        self._prefix = string[: -len(self._suffix)]
        # ex: "--query" is a flag with a prefix of "--" and a suffix of "query"

    def __str__(self) -> str:
        return self._prefix + self._suffix

    @property
    def prefix(self) -> str:
        return self._prefix

    @property
    def suffix(self) -> str:
        return self._suffix
