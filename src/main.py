import argparse

from . import commands


def insight_cli() -> None:
    parser = argparse.ArgumentParser(
        description="insight",
        formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=30),
    )

    commands.add_initialize_command(parser)

    commands.add_query_command(parser)

    commands.add_uninitialize_command(parser)

    commands.add_version_command(parser)

    args = parser.parse_args()

    if args.initialize:
        commands.initialize()

    elif args.query:
        query_string: str = args.query
        commands.query(query_string)

    elif args.uninitialize:
        commands.uninitialize()

    elif args.version:
        commands.version()


if __name__ == "__main__":
    insight_cli()
