from insight_cli.cli.cli_parser import CLIParser
from insight_cli.commands.base.command import Command


class CLI:
    @staticmethod
    def _raise_for_invalid_args(commands: list[Command], description: str) -> None:
        CLI._raise_for_invalid_commands(commands)
        CLI._raise_for_invalid_description(description)

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

    def __init__(self, commands: list[Command], description: str):
        CLI._raise_for_invalid_args(commands, description)
        self._parser = CLIParser(commands, description)

    def run(self) -> None:
        self._parser.parse_arguments()

        for command, command_executor_args in self._parser.invoked_commands_with_args:
            command.execute(*command_executor_args)
