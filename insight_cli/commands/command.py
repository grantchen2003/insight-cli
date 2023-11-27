import collections, inspect


class Command:
    _PREFIXES = ["--", "-"]

    @staticmethod
    def sort(commands: "list[Command]") -> "list[Command]":
        return sorted(
            commands,
        )

    @staticmethod
    def _raise_for_invalid_description(description: str) -> None:
        if not isinstance(description, str):
            raise TypeError("description must be a str")

        if description.strip() == "":
            raise ValueError("description cannot be empty")

    @staticmethod
    def _get_prefix_to_flags(flags: list["Command.Flag"]) -> dict:
        prefix_to_flags = collections.defaultdict(list)

        for flag in flags:
            prefix_to_flags[flag.prefix].append(flag)

        return prefix_to_flags

    @staticmethod
    def _generate_name(flags: list["Command.Flag"]) -> str:
        prefix = "--"
        prefix_to_flags = Command._get_prefix_to_flags(flags)

        if len(prefix_to_flags[prefix]) != 1:
            raise ValueError(f"There is not exactly one suffix for the {prefix} prefix")

        return prefix_to_flags[prefix][0].suffix

    @classmethod
    def _raise_for_invalid_flags(cls, flags: list["Command.Flag"]) -> None:
        min_flag_count, max_flag_count = 1, len(cls._PREFIXES)

        if len(flags) not in range(min_flag_count, max_flag_count + 1):
            raise ValueError(
                f"There must be between {min_flag_count} and {max_flag_count} flags (inclusive)"
            )

        prefix_to_flags = Command._get_prefix_to_flags(flags)

        for i in range(len(flags)):
            prefix = cls._PREFIXES[i]
            flags = prefix_to_flags[prefix]
            if len(flags) != 1:
                raise ValueError(
                    f"The {prefix} prefix does not map to exactly one suffix"
                )

    def __init__(self, flags: list[str], description: str, handler: dict):
        flags = [Command.Flag(flag) for flag in flags]
        Command._raise_for_invalid_description(description)
        Command._raise_for_invalid_flags(flags)
        self._flags: list[Command.Flag] = flags
        self._name: str = Command._generate_name(flags)
        self._description: str = description
        self._handler: Command.Handler = Command.Handler(**handler)

    def __lt__(self, other: "Command") -> bool:
        return self._name < other.name

    @property
    def name(self) -> str:
        return self._name

    @property
    def flags(self) -> list["Command.Flag"]:
        return self._flags

    @property
    def description(self) -> str:
        return self._description

    @property
    def handler(self) -> "Command.Handler":
        return self._handler

    class Flag:
        @staticmethod
        def _raise_for_invalid_flag(string: str):
            if not isinstance(string, str):
                raise TypeError("flag must be a str")

            if string.strip() != string or string == "" or string[0] != "-":
                raise ValueError("string is not in a flag format")

        def __init__(self, string: str):
            Command.Flag._raise_for_invalid_flag(string)
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

    class Handler:
        @staticmethod
        def _raise_for_invalid_params(params):
            if not isinstance(params, list):
                raise TypeError("params must be a list")

            for param in params:
                if "type" not in param:
                    raise KeyError("type key required")

                if "name" not in param:
                    raise KeyError("name key required")

        @staticmethod
        def _raise_for_invalid_function(function):
            if not inspect.isfunction(function):
                raise TypeError("function must be a function")

        @staticmethod
        def _raise_for_params_function_mismatch(params, function):
            if len(params) != len(inspect.signature(function).parameters):
                raise ValueError(
                    "The number of params don't match the number of function parameters"
                )

        def __init__(self, params, function):
            Command.Handler._raise_for_invalid_params(params)
            Command.Handler._raise_for_invalid_function(function)
            Command.Handler._raise_for_params_function_mismatch(params, function)

            self._params = params
            self._function = function

        def __call__(self, *args, **kwargs):
            return self._function(*args, **kwargs)

        @property
        def has_params(self) -> bool:
            return len(self._params) != 0

        @property
        def num_params(self) -> int:
            return len(self._params)

        @property
        def params(self) -> list[dict]:
            return self._params.copy()

        @property
        def param_names(self):
            return [param["name"] for param in self._params]

        @property
        def param_types(self):
            return [param["type"] for param in self._params]
