import collections
import inspect

# TODO:
# make some of the Command.Flag static methods util methods
# make this prefix hierarchy its own ds
# refactor


class Command:
    # general mapping:
    # prefix => [list1, list2, list3, ...] where list_i = [s1, s2, ...]

    _PREFIX_DEPENDENCIES = {
        # in order for the command to use the "--" flag, nothing is required
        "--": [],
        # in order for the command use the "-" flag, the command has to already use
        # all flags in ["--"]
        "-": [["--"]],
        # in order for the command use the "---" flag, the command has to either
        # already use all flags in ["-"] or already use all flags in ["--"]
        "---": [["-"], ["--"]],
        # in order for the command use the "----" flag, the command has to either
        # already use all flags in ["-"] or already use all flags in ["--", "---"]
        "----": [["-"], ["--", "---"]]
    }  # make sure this isn't cyclic,
    # ensure any flags on the left are also on the right(or maybe auto default them to no dependencies)

    _PREFIXES = ["--", "-", "---"]

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
        prefix = "--"  # [prefix] is the prefix of the flag whose name will be the command's name
        prefix_to_flags = Command._get_prefix_to_flags(flags)

        if len(prefix_to_flags[prefix]) != 1:
            raise ValueError(f"There is not exactly one suffix for the {prefix} prefix")

        return prefix_to_flags[prefix][0].name

    @classmethod
    def _raise_for_invalid_prefix_dependency(cls):
        pass

    @classmethod
    def _raise_for_invalid_flags(cls, flags: list["Command.Flag"]) -> None:
        prefixes = cls._PREFIXES
        min_flag_count, max_flag_count = 1, len(prefixes)

        if len(flags) not in range(min_flag_count, max_flag_count + 1):
            raise ValueError(
                f"There must be between {min_flag_count} and {max_flag_count} flags (inclusive)"
            )

        prefix_to_flags = Command._get_prefix_to_flags(flags)
        # prefixes[0] ... prefixes[i - 1] must map to exactly 1 flag in order for
        # prefixes[i] to be used.
        # ensure that prefixes[0], prefixes[1], ..., prefixes[len(flags) - 1]
        # each map to exactly one flag.
        for i in range(len(flags)):
            prefix = prefixes[i]
            flags = prefix_to_flags[prefix]
            if len(flags) != 1:
                raise ValueError(
                    f"The {prefix} prefix does not map to exactly one suffix"
                )

    def __init__(self, flags: list[str], description: str, handler: dict):
        flags = [Command.Flag(flag, Command._PREFIXES) for flag in flags]
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
        def _get_suffix(string: str, prefix) -> str:
            return string[len(prefix):]

        @staticmethod
        def _get_matching_prefixes(string: str, prefixes: list[str]) -> list[str]:
            return [prefix for prefix in prefixes if string.startswith(prefix)]

        @staticmethod
        def _get_matching_suffixes(string: str, matching_prefixes: list[str]) -> list[str]:
            return [
                Command.Flag._get_suffix(string, matching_prefix)
                for matching_prefix in matching_prefixes
            ]

        @staticmethod
        def _raise_for_invalid_args(string: str, prefixes: list[str]):
            if not isinstance(string, str):
                raise TypeError("flag must be a str")

            if string.strip() != string:
                raise ValueError("string cannot be cannot have leading/trailing whitespaces")

            if string == "":
                raise ValueError("string cannot be empty string")

            matching_prefixes = Command.Flag._get_matching_prefixes(string, prefixes)

            if len(matching_prefixes) == 0:
                raise ValueError("no prefix matched")

            matched_suffixes = Command.Flag._get_matching_suffixes(string, matching_prefixes)

            if all(matched_suffix == "" for matched_suffix in matched_suffixes):
                raise ValueError("suffix cannot be empty")

        @staticmethod
        def _get_longest_matching_prefix(string: str, prefixes: list[str]) -> str:
            matching_prefixes = Command.Flag._get_matching_prefixes(string, prefixes)
            longest_matching_prefix = max(matching_prefixes, key=len)
            return longest_matching_prefix

        def __init__(self, string: str, prefixes: list[str]):
            Command.Flag._raise_for_invalid_args(string, prefixes)
            self._prefix = Command.Flag._get_longest_matching_prefix(string, prefixes)
            self._suffix = Command.Flag._get_suffix(string, self._prefix)

        def __str__(self) -> str:
            return self._prefix + self._suffix

        @property
        def prefix(self) -> str:
            return self._prefix

        @property
        def name(self) -> str:
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
