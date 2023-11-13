from pathlib import Path

import argparse
import commands
import config
import os


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
        help="creates a code-seek repository in the current directory",
    )

    parser.add_argument(
        "-q",
        "--query",
        type=str,
        help="shows files in the current repository that satisfy the given natural language query",
    )

    parser.add_argument(
        "-u",
        "--uninitialize",
        action="store_true",
        help="deletes code-seek repositories in the current directory",
    )

    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        help="shows the current version of insight",
    )

    args = parser.parse_args()

    if args.initialize:
        codebase_dir_path = Path.cwd()
        commands.codebase.initialize(codebase_dir_path)

    elif args.query:
        query = args.query
        print(f"querystring: {query}")

    elif args.uninitialize:
        codebase_dir_path = Path.cwd()
        commands.codebase.uninitialize(codebase_dir_path)

    elif args.version:
        print("insight 0.0.0")


if __name__ == "__main__":
    main()
