from argparse import ArgumentParser


def add_version_command(parser: ArgumentParser) -> None:
    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        help="shows the current version of insight",
    )


def handle_version_command() -> None:
    print("insight 0.0.0")
