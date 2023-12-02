from insight_cli.commands.base.command import Command
from insight_cli.cli.interfaces.cli_argument_validator_interface import (
    CLIArgumentValidatorInterface,
)


class CLIArgumentValidator(CLIArgumentValidatorInterface):
    @staticmethod
    def raise_for_invalid_args(commands: list[Command], description: str) -> None:
        CLIArgumentValidator._raise_for_invalid_commands(commands)
        CLIArgumentValidator._raise_for_invalid_description(description)

    @staticmethod
    def _raise_for_invalid_description(description: str) -> None:
        if not isinstance(description, str):
            raise TypeError("description must be a str")

        if description.strip() == "":
            raise ValueError("description cannot be empty")

    @staticmethod
    def _raise_for_invalid_commands(commands: list[Command]) -> None:
        if not isinstance(commands, list):
            raise TypeError("commands must be a list")

        if not commands:
            raise ValueError("commands must be a non-empty list")

        if any(not isinstance(command, Command) for command in commands):
            raise TypeError("each element in commands must be of type Command")
