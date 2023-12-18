from abc import ABC, abstractmethod
from typing import Callable
import inspect, typing

from .flag import Flag


class Command(ABC):
    _MIN_NUM_REQUIRED_FLAGS = 1

    @classmethod
    def _raise_for_invalid_flags(cls, flags: list[str]) -> None:
        if not isinstance(flags, list):
            raise TypeError(f"{flags} must be a list")

        if len(flags) < cls._MIN_NUM_REQUIRED_FLAGS:
            raise ValueError(f"at least {cls._MIN_NUM_REQUIRED_FLAGS} flag(s) required")

        if any(not isinstance(flag, str) for flag in flags):
            raise TypeError(f"every flag in {flags} must be of type str")

        if len(flags) != len(set(flags)):
            raise ValueError(f"every flag in {flags} must be unique")

    @staticmethod
    def _raise_for_invalid_description(description: str) -> None:
        if not isinstance(description, str):
            raise TypeError(f"{description} must be of type str")

        if description.strip() == "":
            raise ValueError(f"{description} must not be a whitespace string")

    @staticmethod
    def _raise_for_invalid_executor(executor: Callable) -> None:
        param_names = inspect.signature(executor).parameters
        param_types = typing.get_type_hints(executor)
        for param_name in param_names:
            if param_name not in param_types:
                raise ValueError(
                    f"the {executor} parameter '{param_name}' does not have a type"
                )

    def __init__(self, flags: list[str], description: str):
        Command._raise_for_invalid_flags(flags)
        Command._raise_for_invalid_description(description)
        Command._raise_for_invalid_executor(self.execute)

        self._flags: list[Flag] = [Flag(flag) for flag in flags]
        self._description: str = description

    @abstractmethod
    def execute(self, *args, **kwargs):
        pass

    @property
    def description(self) -> str:
        return self._description

    @property
    def flags(self) -> list[Flag]:
        return self._flags

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
    def executor_param_names(self) -> list[str]:
        return [param["name"] for param in self.executor_params]

    @property
    def executor_param_types(self) -> list:
        return [param["type"] for param in self.executor_params]
