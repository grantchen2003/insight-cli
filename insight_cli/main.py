from insight_cli.cli import CLI
from insight_cli.cli.cli_parser import CLIParser
from insight_cli.commands.initialize_command import InitializeCommand
from insight_cli.commands.query_command import QueryCommand
from insight_cli.commands.uninitialize_command import UninitializeCommand
from insight_cli.commands.version_command import VersionCommand


def main() -> None:
    cli = CLI(
        commands=[
            InitializeCommand(),
            QueryCommand(),
            UninitializeCommand(),
            VersionCommand(),
        ],
        description="insight-cli",
        parser=CLIParser,
    )

    cli.run()


if __name__ == "__main__":
    main()
