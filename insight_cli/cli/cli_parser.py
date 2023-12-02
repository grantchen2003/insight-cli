from typing import Any, Callable, TypedDict
import argparse, operator

from insight_cli.cli.interfaces.cli_parser_interface import CLIParserInterface
from insight_cli.cli.cli_argument_validator import CLIArgumentValidator
from insight_cli.commands.base.command import Command


class ParsedCommand(TypedDict):
    command: Command
    get_executor_args: Callable
    name: str
    flag_strings: list[str]
    options: dict


class CLIParser(CLIParserInterface):
    # make this function cleaner, handle prefix priority better
    @staticmethod
    def _parse_command(command: Command) -> ParsedCommand:
        command_name_flag_prefix = "--"

        def get_command_executor_args(command_args: str) -> list[Any]:
            return [
                param_type(arg)
                for arg, param_type in zip(command_args, command.executor_param_types)
            ]

        parsed_command = {
            "command": command,
            "get_executor_args": get_command_executor_args,
            "name": [
                flag.name
                for flag in command.flags
                if flag.prefix == command_name_flag_prefix
            ][0],
            "flag_strings": [str(flag) for flag in command.flags],
        }

        if command.has_executor_params:
            parsed_command["options"] = {
                "help": command.description,
                "metavar": tuple(
                    [f"<{param_name}>" for param_name in command.executor_param_names]
                ),
                "nargs": command.num_executor_params,
            }

        else:
            parsed_command["options"] = {
                "action": "store_const",
                "const": [],
                "help": command.description,
            }

        return parsed_command

    def __init__(self, commands: list[Command], description: str, max_width: int = 50):
        CLIArgumentValidator.raise_for_invalid_args(commands, description)
        self._arguments: argparse.Namespace = None
        self._parsed_commands: dict[str, ParsedCommand] = {}
        self._parser = argparse.ArgumentParser(
            description=description,
            formatter_class=lambda prog: argparse.HelpFormatter(
                prog, max_help_position=max_width
            ),
        )
        self._add_commands(commands)

    def _add_commands(self, commands: list[Command]) -> None:
        parsed_commands = [CLIParser._parse_command(command) for command in commands]

        parsed_commands.sort(key=operator.itemgetter("name"))

        for parsed_command in parsed_commands:
            if parsed_command["name"] in self._parsed_commands:
                raise ValueError(
                    f"A command with a name of {parsed_command['name']} already exists"
                )

            self._parser.add_argument(
                *parsed_command["flag_strings"], **parsed_command["options"]
            )

            self._parsed_commands[parsed_command["name"]] = parsed_command

    def parse_arguments(self) -> None:
        self._arguments = self._parser.parse_args() 

    def get_invoked_commands_and_executor_args(self) -> list[tuple[Command, list[Any]]]:
        invoked_commands_and_executor_args = []

        for command_name, command_args in vars(self._arguments).items():
            command_is_not_invoked = command_args is None
            if command_is_not_invoked:
                continue

            parsed_command = self._parsed_commands[command_name]
            command = parsed_command["command"]
            command_executor_args = parsed_command["get_executor_args"](command_args)

            invoked_commands_and_executor_args.append((command, command_executor_args))

        return invoked_commands_and_executor_args
