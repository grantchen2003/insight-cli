from typing import Any

from insight_cli.commands.base.command import Command


class ParsedCommand():
    def __init__(self, command: Command):
        self._command = command

    def get_executor_args(self, command_args: list[str]) -> list[Any]:
        return [
            param_type(arg)
            for arg, param_type in zip(command_args, self._command.executor_param_types)
        ]

    @property
    def command(self) -> Command:
        return self._command

    @property
    def name(self) -> str:
        command_name_flag_prefix_priority = ["--"]
        for flag_prefix in command_name_flag_prefix_priority:
            for flag in self._command.flags:
                if flag.prefix == flag_prefix:
                    return flag.name

    @property
    def flag_strings(self) -> list[str]:
        return [str(flag) for flag in self._command.flags]

    @property
    def options(self) -> dict:
        if not self._command.has_executor_params:
            return {
                "action": "store_const",
                "const": [],
                "help": self._command.description,
            }

        return {
            "help": self._command.description,
            "metavar": tuple(
                f"<{param_name}>" for param_name in self._command.executor_param_names
            ),
            "nargs": self._command.num_executor_params,
        }
