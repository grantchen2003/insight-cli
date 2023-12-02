from typing import Any
import argparse

from insight_cli.cli.parsed_command import ParsedCommand
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

        flag_strings = []
        for command in commands:
            parsed_command = ParsedCommand(command)
            flag_strings.extend(parsed_command.flag_strings)

        if len(set(flag_strings)) != len(flag_strings):
            raise ValueError("all flags strings must be unique")

    def __init__(self, commands: list[Command], description: str, max_width: int = 50):
        CLI._raise_for_invalid_args(commands, description)
        self._arguments: argparse.Namespace = argparse.Namespace()
        self._parsed_commands: dict[str, ParsedCommand] = {}
        self._parser: argparse.ArgumentParser = argparse.ArgumentParser(
            description=description,
            formatter_class=lambda prog: argparse.HelpFormatter(
                prog, max_help_position=max_width
            ),
        )
        self._add_commands(commands)

    def _add_commands(self, commands: list[Command]) -> None:
        parsed_commands = [ParsedCommand(command) for command in commands]

        parsed_commands.sort(key=lambda parsed_command: parsed_command.name)

        for parsed_command in parsed_commands:
            self._parser.add_argument(
                *parsed_command.flag_strings, **parsed_command.options
            )

            self._parsed_commands[parsed_command.name] = parsed_command

    def parse_arguments(self) -> None:
        self._arguments: argparse.Namespace = self._parser.parse_args()

    def execute_invoked_commands(self) -> None:
        for command_name, command_args in vars(self._arguments).items():
            command_is_not_invoked = command_args is None
            if command_is_not_invoked:
                continue

            parsed_command: ParsedCommand = self._parsed_commands[command_name]
            command: Command = parsed_command.command
            command_executor_args: list[Any] = parsed_command.get_executor_args(
                command_args
            )

            command.execute(*command_executor_args)
