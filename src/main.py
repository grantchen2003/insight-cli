import argparse

from . import commands


def insight_cli() -> None:
    parser = argparse.ArgumentParser(
        description="insight",
        formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=30),
    )

    commands.add_initialize(parser)

    commands.add_query(parser)

    commands.add_uninitialize(parser)

    commands.add_version(parser)

    args = parser.parse_args()

    if args.initialize:
        commands.handle_initialize()

    elif args.query:
        query_string: str = args.query
        commands.handle_query(query_string)

    elif args.uninitialize:
        commands.handle_uninitialize()

    elif args.version:
        commands.handle_version()


if __name__ == "__main__":
    insight_cli()
