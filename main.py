import argparse
import commands


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
        commands.initialize_codebase()

    elif args.query:
        commands.query_codebase(args.query)

    elif args.uninitialize:
        commands.uninitialize_codebase()

    elif args.version:
        commands.version()


if __name__ == "__main__":
    main()
