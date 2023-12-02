import inspect, typing
from abc import ABC, abstractmethod

from insight_cli.commands.base.command_flag import CommandFlag


class Command(ABC):
    _MIN_NUM_REQUIRED_FLAGS = 1

    @staticmethod
    def _raise_for_invalid_args(flags: list[str], description: str) -> None:
        Command._raise_for_invalid_flags(flags)
        Command._raise_for_invalid_description(description)

    @classmethod
    def _raise_for_invalid_flags(cls, flags: list[str]) -> None:
        if not isinstance(flags, list):
            raise TypeError("flags must be a list")

        if len(flags) < cls._MIN_NUM_REQUIRED_FLAGS:
            raise ValueError(
                f"There must be at least {cls._MIN_NUM_REQUIRED_FLAGS} flags"
            )

        if any(not isinstance(flag, str) for flag in flags):
            raise TypeError("every flag in flags must be of type string")

        if len(flags) != len(set(flags)):
            raise ValueError("the flag strings must all be unique")

    @staticmethod
    def _raise_for_invalid_description(description: str) -> None:
        if not isinstance(description, str):
            raise TypeError("description must be a str")

        if description.strip() == "":
            raise ValueError("description cannot be empty")

    @abstractmethod
    def execute(self, *args, **kwargs):
        pass

    def __init__(self, flags: list[str], description: str):
        Command._raise_for_invalid_args(flags, description)
        self._flags: list[CommandFlag] = [CommandFlag(flag) for flag in flags]
        self._description: str = description

    @property
    def flags(self) -> list[CommandFlag]:
        return self._flags

    @property
    def description(self) -> str:
        return self._description

    @property
    def has_executor_params(self) -> bool:
        return self.num_executor_params != 0

    @property
    def num_executor_params(self) -> int:
        return len(self.executor_params)

    @property
    def executor_params(self) -> list[dict]:
        param_names = inspect.signature(self.execute).parameters
        param_types = typing.get_type_hints(self.execute)
        return [
            {"name": param_name, "type": param_types[param_name]}
            for param_name in param_names
        ]

    @property
    def executor_param_names(self):
        return [param["name"] for param in self.executor_params]

    @property
    def executor_param_types(self):
        return [param["type"] for param in self.executor_params]
