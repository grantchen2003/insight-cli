from pathlib import Path

from src.commands.classes import Command
from src.core import repository, dot_insight_dir
from src.utils import Color


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
    repository_dir_path = Path.cwd()

    dot_insight_dir_path: Path = repository_dir_path / dot_insight_dir.get_dir_name()

    if not dot_insight_dir.is_valid(dot_insight_dir_path):
        print(Color.red("The current directory is not an insight repository."))
        return

    matches = repository.query(repository_dir_path, query_string)

    num_matches = len(matches)

    if num_matches == 0:
        matches_found_sentence = f"{num_matches} matches found"

    elif num_matches == 1:
        matches_found_sentence = f"{num_matches} match found in the following file:"

    else:
        matches_found_sentence = f"{num_matches} matches found in the following files:"

    print(Color.yellow(matches_found_sentence))

    for match in matches:
        if match["start_line"] == match["end_line"]:
            line_numbers = f"Line {match['start_line']}"
        else:
            line_numbers = f"Line {match['start_line']} - {match['end_line']}"

        print(match["path"])
        print(f"\t{line_numbers}: {Color.green(match['content'])}")
