from typing import Any, Dict, Iterable
import argparse

from insight_cli.commands.command import Command


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

    @staticmethod
    def _parse_command(command: Command) -> dict:
        parsed_command = {"flag_strings": [str(flag) for flag in command.flags]}

        if command.handler.has_params:
            parsed_command["options"] = {
                "help": command.description,
                "metavar": tuple(
                    [f"<{param_name}>" for param_name in command.handler.param_names]
                ),
                "nargs": command.handler.num_params,
            }

        else:
            parsed_command["options"] = {
                "action": "store_const",
                "const": [],
                "help": command.description,
            }

        return parsed_command

    def __init__(self, commands: list[Command], description: str, max_width: int = 50):
        CLI._raise_for_invalid_args(commands, description)
        self._arguments = argparse.Namespace()
        self._commands: Dict[str, Command] = {}
        self._parser = argparse.ArgumentParser(
            description=description,
            formatter_class=lambda prog: argparse.HelpFormatter(
                prog, max_help_position=max_width
            ),
        )
        self._add_commands(commands, sort=True)

    def _add_commands(self, commands: list[Command], sort: bool = True) -> None:
        if sort:
            commands = sorted(commands)

        for command in commands:
            self._add_command(command)

    def _add_command(self, command: Command) -> None:
        if command.name in self._commands:
            raise ValueError("Cannot add the same command twice")

        parsed_command = CLI._parse_command(command)
        self._parser.add_argument(*parsed_command["flag_strings"], **parsed_command["options"])

        self._commands[command.name] = command

    def _get_command_handler_args(self, command_name: str, command_args: str) -> list[Any]:
        arg_and_param_type_pairs = zip(command_args, self._commands[command_name].handler.param_types)
        return [param_type(arg) for arg, param_type in arg_and_param_type_pairs]

    def _get_invoked_command_name_and_args(self):
        for command_name, command_args in vars(self._arguments).items():
            command_is_invoked = command_args is not None
            if command_is_invoked:
                yield command_name, command_args

    def parse_arguments(self) -> None:
        self._arguments = self._parser.parse_args()

    def execute_invoked_commands(self) -> None:
        for command_name, command_args in self._get_invoked_command_name_and_args():
            command_handler_args = self._get_command_handler_args(
                command_name, command_args
            )
            self._commands[command_name].handler(*command_handler_args)
