from typing import Any, Dict
import argparse

from insight_cli.commands.base.command import Command

# TODO
# handle prefix priority better
# merge _get_command_executor_args with _parse_command, make it into its own class


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
        command_name_flag_prefix = "--"

        parsed_command = {
            "command": command,
            "name": [
                flag.name for flag in command.flags
                if flag.prefix == command_name_flag_prefix
            ][0],
            "flag_strings": [str(flag) for flag in command.flags]
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

    @staticmethod
    def _get_command_executor_args(command: Command, command_args: str) -> list[Any]:
        return [param_type(arg) for arg, param_type in zip(command_args, command.executor_param_types)]

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
        self._add_commands(commands)

    def _add_commands(self, commands: list[Command]) -> None:
        parsed_commands = [CLI._parse_command(command) for command in commands]
        
        parsed_commands.sort(key=lambda parsed_command: parsed_command["name"])
        
        for parsed_command in parsed_commands:
            if parsed_command["name"] in self._commands:
                raise ValueError(f"A command with a name of {parsed_command['name']} already exists")

            self._parser.add_argument(*parsed_command["flag_strings"], **parsed_command["options"])

            self._commands[parsed_command["name"]] = parsed_command["command"]

    def _get_invoked_command_name_and_args(self):
        for command_name, command_args in vars(self._arguments).items():
            command_is_invoked = command_args is not None
            if command_is_invoked:
                yield command_name, command_args

    def parse_arguments(self) -> None:
        self._arguments = self._parser.parse_args()

    def execute_invoked_commands(self) -> None:
        for command_name, command_args in self._get_invoked_command_name_and_args():
            command = self._commands[command_name]
            command.execute(*CLI._get_command_executor_args(command, command_args))
