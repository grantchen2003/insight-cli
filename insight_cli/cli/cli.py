from typing import Callable, TypedDict
import argparse

from insight_cli.commands.base.command import Command


class ParsedCommand(TypedDict):
    command: Command
    flag_names: list[str]
    flag_strings: list[str]
    get_executor_args: Callable
    name: str
    options: dict


class CLI:
    @staticmethod
    def _raise_for_invalid_args(commands: list[Command], description: str) -> None:
        CLI._raise_for_invalid_commands(commands)
        CLI._raise_for_invalid_description(description)

    @staticmethod
    def _raise_for_invalid_description(description: str) -> None:
        if not isinstance(description, str):
            raise TypeError("[description] must be a str")

    @staticmethod
    def _raise_for_invalid_commands(commands: list[Command]) -> None:
        if not isinstance(commands, list):
            raise TypeError("[commands] must be of type list")

        if not commands:
            raise ValueError("[commands] must be a non-empty list")

        if any(not isinstance(command, Command) for command in commands):
            raise TypeError("each command in [commands] must be of type Command")

        flag_strings, flag_names = [], []
        for command in commands:
            parsed_command = CLI._parse_command(command)
            flag_strings.extend(parsed_command["flag_strings"])
            flag_names.extend(parsed_command["flag_names"])

        if len(set(flag_strings)) != len(flag_strings):
            raise ValueError("all flag strings in [commands] must be unique")

        if len(set(flag_names)) != len(flag_names):
            raise ValueError("all flag names in [commands] must be unique")

    @staticmethod
    def _parse_command(command: Command) -> ParsedCommand:
        def get_name() -> str:
            """
            [prefixes] contains the prefixes sorted in descending
            priority. Priorities are determined the argparse library.

            The name of the command flag with the highest priority
            prefix will be the name of the command.
            """
            prefixes = ["--", "---", "-"]

            for prefix in prefixes:
                for flag in command.flags:
                    if flag.prefix == prefix:
                        return flag.name

            raise ValueError("No name found")

        def get_executor_args(command_args: list[str]) -> list:
            return [
                param_type(arg)
                for arg, param_type in zip(command_args, command.executor_param_types)
            ]

        def get_flag_names() -> list[str]:
            return [flag.name for flag in command.flags]

        def get_flag_strings() -> list[str]:
            return [str(flag) for flag in command.flags]

        def get_options() -> dict:
            if command.has_executor_params:
                return {
                    "help": command.description,
                    "metavar": tuple(
                        f"<{param_name}>" for param_name in command.executor_param_names
                    ),
                    "nargs": command.num_executor_params,
                }

            return {
                "action": "store_const",
                "const": [],
                "help": command.description,
            }

        parsed_command = {
            "command": command,
            "get_executor_args": get_executor_args,
            "name": get_name(),
            "flag_names": get_flag_names(),
            "flag_strings": get_flag_strings(),
            "options": get_options(),
        }

        return parsed_command

    def __init__(self, commands: list[Command], description: str):
        CLI._raise_for_invalid_args(commands, description)
        self._arguments: argparse.Namespace = argparse.Namespace()
        self._parsed_commands: dict[str, ParsedCommand] = {}
        self._parser: argparse.ArgumentParser = argparse.ArgumentParser(
            description=description,
            formatter_class=lambda prog: argparse.HelpFormatter(
                prog, max_help_position=50
            ),
        )
        self._add_commands(commands)

    def _add_commands(self, commands: list[Command]) -> None:
        sorted_parsed_commands: list[ParsedCommand] = sorted(
            [CLI._parse_command(command) for command in commands],
            key=lambda parsed_command: parsed_command["name"],
        )

        for parsed_command in sorted_parsed_commands:
            self._parser.add_argument(
                *parsed_command["flag_strings"], **parsed_command["options"]
            )
            self._parsed_commands[parsed_command["name"]] = parsed_command

    def parse_arguments(self) -> None:
        self._arguments: argparse.Namespace = self._parser.parse_args()

    def execute_invoked_commands(self) -> None:
        for command_name, command_args in vars(self._arguments).items():
            command_is_not_invoked = command_args is None
            if command_is_not_invoked:
                continue

            parsed_command = self._parsed_commands[command_name]
            command = parsed_command["command"]
            command_executor_args = parsed_command["get_executor_args"](command_args)

            command.execute(*command_executor_args)
