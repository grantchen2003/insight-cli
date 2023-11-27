from pathlib import Path

from insight_cli.commands.command import Command
from insight_cli.core import repository, dot_insight_dir
from insight_cli.utils import Color


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

    print_matches(matches)


def print_matches(matches) -> None:
    num_matches = len(matches)

    if num_matches == 0:
        print(Color.yellow(f"{num_matches} matches found"))

    elif num_matches == 1:
        print(Color.yellow(f"{num_matches} match found in the following file:"))

    else:
        print(Color.yellow(f"{num_matches} matches found in the following files:"))

    for i, match in enumerate(matches):
        is_first_match = i == 0
        
        match_text = "" if is_first_match else "\n"
        
        match_text += f"{match["path"]}\n"
        
        if match["start_line"] == match["end_line"]:
            match_text += f"\tLine {match['start_line']}: {Color.green(match['content'])}"
        else:
            match_text += f"\tLine {match['start_line']} - {match['end_line']}: {Color.green(match['content'])}"
            
        print(match_text)
