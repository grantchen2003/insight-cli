from pathlib import Path
import argparse
import os

import core
import config


def main() -> None:
    config.load_environment_variables(os.environ.get("ENV"))

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
        repository_dir_path = Path.cwd()
        core.repository.initialize(repository_dir_path)

    elif args.query:
        query = args.query
        print(f"querystring: {query}")

    elif args.uninitialize:
        repository_dir_path = Path.cwd()
        core.repository.uninitialize(repository_dir_path)

    elif args.version:
        print("insight 0.0.0")


if __name__ == "__main__":
    main()
