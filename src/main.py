import argparse

from . import commands


def insight_cli() -> None:
    parser = argparse.ArgumentParser(
        description="insight",
        formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=30),
    )

    parser.add_argument(
        "-i",
        "--initialize",
        action="store_true",
        help="initializes the current directory as an insight repository",
    )

    parser.add_argument(
        "-q",
        "--query",
        type=str,
        help="shows files in the current insight repository that satisfy the given natural language query",
    )

    parser.add_argument(
        "-u",
        "--uninitialize",
        action="store_true",
        help="uninitializes the current directory as an insight repository",
    )

    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        help="shows the current version of insight",
    )

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
