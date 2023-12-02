class CommandFlag:
    _MIN_NAME_LENGTH = 1
    _MIN_PREFIX_LENGTH = 1
    _PREFIX_CHAR = '-'

    @classmethod
    def _raise_for_invalid_args(cls, string: str) -> None:
        if not isinstance(string, str):
            raise TypeError("string must be a str")

        if any(char == " " for char in string):
            raise ValueError(
                "string cannot be cannot have any whitespaces"
            )

        if len(string) < cls._MIN_PREFIX_LENGTH + cls._MIN_NAME_LENGTH:
            raise ValueError(
                f"string must have a length of at least {cls._MIN_PREFIX_LENGTH + cls._MIN_NAME_LENGTH}"
            )

        if any(string[i] != cls._PREFIX_CHAR for i in range(cls._MIN_PREFIX_LENGTH)):
            raise ValueError(
                f"the first {cls._MIN_PREFIX_LENGTH} characters of the string must all be '{cls._PREFIX_CHAR}'"
            )

        name = string.lstrip(CommandFlag._PREFIX_CHAR)
        if len(name) < cls._MIN_NAME_LENGTH:
            raise ValueError(f"string must have a name of at least length {cls._MIN_NAME_LENGTH}")

    def __init__(self, string: str):
        CommandFlag._raise_for_invalid_args(string)
        self._string = string

    def __str__(self) -> str:
        return self._string

    @property
    def prefix(self) -> str:
        return self._string[:-len(self.name)]

    @property
    def name(self) -> str:
        return self._string.lstrip(CommandFlag._PREFIX_CHAR)
