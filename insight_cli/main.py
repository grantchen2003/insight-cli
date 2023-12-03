from insight_cli.cli import CLI
from insight_cli.commands import InitializeCommand
from insight_cli.commands import QueryCommand
from insight_cli.commands import UninitializeCommand
from insight_cli.commands import VersionCommand


def main() -> None:
    cli = CLI(
        commands=[
            InitializeCommand(),
            QueryCommand(),
            UninitializeCommand(),
            VersionCommand(),
        ],
        description="insight-cli",
    )

    cli.parse_arguments()

    cli.execute_invoked_commands()


if __name__ == "__main__":
    main()
