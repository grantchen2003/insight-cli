from argparse import ArgumentParser


def add_query_command(parser: ArgumentParser) -> None:
    parser.add_argument(
        "-q",
        "--query",
        type=str,
        help="shows files in the current insight repository that satisfy the given natural language query",
    )


def handle_query_command(query_string: str) -> None:
    print(f"query_string: {query_string}")
