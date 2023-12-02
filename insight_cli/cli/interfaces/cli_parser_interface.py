from abc import ABC, abstractmethod
from typing import Any

from insight_cli.commands.base.command import Command


class CLIParserInterface(ABC):
    @abstractmethod
    def parse_arguments(self) -> list[tuple[Command, list[Any]]]:
        pass

    # @abstractmethod
    # def get_invoked_commands_and_executor_args(self) -> list[tuple[Command, list[Any]]]:
    #     pass
