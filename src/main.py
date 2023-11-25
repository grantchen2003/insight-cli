from src.cli import CLI
from src.commands import (
    create_initialize_command,
    create_uninitialize_command,
    create_query_command,
    create_version_command,
)


def insight_cli() -> None:
    commands = [
        create_initialize_command(),
        create_query_command(),
        create_uninitialize_command(),
        create_version_command(),
    ]

    cli = CLI("insight-cli")

    cli.add_commands(commands)

    arguments = cli.parse_arguments()

    cli.execute_commands(arguments)


if __name__ == "__main__":
    insight_cli()
