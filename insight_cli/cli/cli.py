from insight_cli.cli.interfaces.cli_parser_interface import CLIParserInterface
from insight_cli.cli.cli_argument_validator import CLIArgumentValidator
from insight_cli.commands.base.command import Command


class CLI:
    def __init__(
        self, commands: list[Command], description: str, cli_parser: CLIParserInterface
    ):
        CLIArgumentValidator.raise_for_invalid_args(commands, description)
        self._parser: CLIParserInterface = cli_parser(commands, description)

    def run(self) -> None:
        invoked_commands_and_executor_args = self._parser.parse_arguments()

        # invoked_commands_and_executor_args = (
        #     self._parser.get_invoked_commands_and_executor_args()
        # )

        for command, command_executor_args in invoked_commands_and_executor_args:
            command.execute(*command_executor_args)
