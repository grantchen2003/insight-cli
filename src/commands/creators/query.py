from src.commands.classes import Command


def create_query_command() -> Command:
    return Command(
        flags=["-q", "--query"],
        description="shows files in the current insight repository that satisfy the given natural language query",
        handler={
            "params": [{"name": "query", "type": str}],
            "function": handle_query_command,
        },
    )


def handle_query_command(query_string: str) -> None:
    print(f"query_string: {query_string}")
