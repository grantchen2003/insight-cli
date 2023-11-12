import argparse
import codebase
import os
from pathlib import Path
from config import load_environment_variables


def main() -> None:
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
        codebase.initialize(codebase_dir_path)

    elif args.query:
        query = args.query
        print(f"querystring: {query}")

    elif args.uninitialize:
        codebase_dir_path = Path.cwd()
        codebase.uninitialize(codebase_dir_path)

    elif args.version:
        print("insight 0.0.0")


if __name__ == "__main__":
    load_environment_variables(os.environ.get("ENV"))
    main()
