class Flag:
    _MIN_NAME_LENGTH = 1
    _MIN_PREFIX_LENGTH = 1
    _PREFIX_CHAR = "-"

    @classmethod
    def _raise_for_invalid_args(cls, string: str) -> None:
        if not isinstance(string, str):
            raise TypeError(f"{string} must be of type str")

        if any(char == " " for char in string):
            raise ValueError(f"{string} cannot contain any whitespaces")

        if len(string) < cls._MIN_PREFIX_LENGTH + cls._MIN_NAME_LENGTH:
            raise ValueError(
                f"{string} must have length of at least {cls._MIN_PREFIX_LENGTH + cls._MIN_NAME_LENGTH}"
            )

        if any(string[i] != cls._PREFIX_CHAR for i in range(cls._MIN_PREFIX_LENGTH)):
            raise ValueError(
                f"the first {cls._MIN_PREFIX_LENGTH} characters of {string} must all be '{cls._PREFIX_CHAR}'"
            )

        name = string.lstrip(Flag._PREFIX_CHAR)
        if len(name) < cls._MIN_NAME_LENGTH:
            raise ValueError(
                f"{string} must have a name of at least length {cls._MIN_NAME_LENGTH}"
            )

    def __init__(self, string: str):
        Flag._raise_for_invalid_args(string)
        self._string = string

    def __str__(self) -> str:
        return self._string

    @property
    def name(self) -> str:
        return self._string.lstrip(Flag._PREFIX_CHAR)

    @property
    def prefix(self) -> str:
        return self._string[: -len(self.name)]
