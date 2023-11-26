from typing import Dict, Any
import argparse

from insight_cli.commands.classes import Command


MAX_HELP_POS = 50


class CLI:
    @staticmethod
    def _get_command_handler_args(command: Command, command_args: str) -> list[Any]:
        arg_and_param_type_pairs = zip(command_args, command.handler.param_types)
        return [param_type(arg) for arg, param_type in arg_and_param_type_pairs]

    @staticmethod
    def _raise_for_invalid_description(description: str) -> None:
        if not isinstance(description, str):
            raise TypeError("description must be a str")

        if description.strip() == "":
            raise ValueError("description cannot be empty")

    @staticmethod
    def _parse_command(command: Command) -> list[list[str], dict[str:Any]]:
        flag_strings: list[str] = [str(flag) for flag in command.flags]

        if command.handler.has_params:
            options = {
                "help": command.description,
                "metavar": tuple(
                    [f"<{param_name}>" for param_name in command.handler.param_names]
                ),
                "nargs": command.handler.num_params,
            }

        else:
            options = {
                "action": "store_const",
                "const": [],
                "help": command.description,
            }

        return [flag_strings, options]

    def __init__(self, description: str):
        CLI._raise_for_invalid_description(description)
        self._commands: Dict[str, Command] = {}
        self._parser = argparse.ArgumentParser(
            description=description,
            formatter_class=lambda prog: argparse.HelpFormatter(
                prog, max_help_position=MAX_HELP_POS
            ),
        )

    def parse_arguments(self) -> argparse.Namespace:
        arguments: argparse.Namespace = self._parser.parse_args()
        return arguments

    def add_commands(self, commands: list[Command], sort: bool = True) -> None:
        if sort:
            commands = sorted(commands)

        for command in commands:
            self.add_command(command)

    def add_command(self, command: Command) -> None:
        if command.name in self._commands:
            raise ValueError("Cannot add the same command twice")

        flag_strings, options = CLI._parse_command(command)
        self._parser.add_argument(*flag_strings, **options)

        self._commands[command.name] = command

    def execute_commands(self, arguments: argparse.Namespace) -> None:
        for command_name, command_args in vars(arguments).items():
            if command_args is not None:
                command_handler_args = CLI._get_command_handler_args(
                    self._commands[command_name], command_args
                )
                self._commands[command_name].handler(*command_handler_args)
