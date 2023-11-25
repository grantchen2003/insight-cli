import collections

from .flag import Flag
from .handler import Handler


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
    def _get_prefix_to_flags(flags: list[Flag]) -> dict:
        prefix_to_flags = collections.defaultdict(list)

        for flag in flags:
            prefix_to_flags[flag.prefix].append(flag)

        return prefix_to_flags

    @staticmethod
    def _generate_name(flags: list[Flag]) -> str:
        prefix = "--"
        prefix_to_flags = Command._get_prefix_to_flags(flags)

        if len(prefix_to_flags[prefix]) != 1:
            raise ValueError(f"There is not exactly one suffix for the {prefix} prefix")

        return prefix_to_flags[prefix][0].suffix

    @classmethod
    def _raise_for_invalid_flags(cls, flags: list[Flag]) -> None:
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
        flags = [Flag(flag) for flag in flags]
        Command._raise_for_invalid_description(description)
        Command._raise_for_invalid_flags(flags)
        self._flags: list[Flag] = flags
        self._name: str = Command._generate_name(flags)
        self._description: str = description
        self._handler: Handler = Handler(**handler)

    def __lt__(self, other: "Command") -> bool:
        return self._name < other.name

    @property
    def name(self) -> str:
        return self._name

    @property
    def flags(self) -> list[Flag]:
        return self._flags

    @property
    def description(self) -> str:
        return self._description

    @property
    def handler(self) -> Handler:
        return self._handler
