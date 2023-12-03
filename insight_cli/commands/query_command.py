from pathlib import Path

from insight_cli.commands.base.command import Command
from insight_cli.repository import Repository
from insight_cli.utils import Color


class QueryCommand(Command):
    @staticmethod
    def _print_matches(matches) -> None:
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

            match_text += f"{match['path']}\n"

            if match["start_line"] == match["end_line"]:
                match_text += (
                    f"\tLine {match['start_line']}: {Color.green(match['content'])}"
                )
            else:
                match_text += f"\tLine {match['start_line']} - {match['end_line']}: {Color.green(match['content'])}"

            print(match_text)

    def __init__(self):
        super().__init__(
            flags=["-q", "--query"],
            description="shows files in the current insight repository that satisfy the given natural language query",
        )

    def execute(self, query_string: str) -> None:
        repository = Repository(Path.cwd())
        
        try:
            matches = repository.query(query_string)
            self._print_matches(matches)

        except FileNotFoundError:
            print(Color.red("The current directory is not an insight repository."))
