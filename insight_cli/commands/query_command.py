from pathlib import Path
import requests

from .base.command import Command
from insight_cli.repository import Repository, FileSizeExceededError, InvalidRepositoryError
from insight_cli.utils import Color


class QueryCommand(Command):
    @staticmethod
    def _print_matches(matches) -> None:
        if matches is None:
            print(Color.red("No matches found"))
            
            return
            
        for i, match in enumerate(matches):
            is_first_match = i == 0

            terminal_output = "" if is_first_match else "\n"

            terminal_output += f"{Path("").resolve() / match['path']}\n"

            if match["start_line"] == match["end_line"]:
                terminal_output += (
                    f"Line {match['start_line']}:\n{Color.green(match['content'])}"
                )

            else:
                terminal_output += f"Line {match['start_line']} - {match['end_line']}:\n{Color.green(match['content'])}"

            print(terminal_output)

    def __init__(self):
        super().__init__(
            flags=["-q", "--query"],
            description="shows the top code snippets in the current insight repository that satisfy the given natural language query",
        )

    def execute(self, query_string: str, limit: int) -> None:
        if limit <= 0:
            print(Color.red("Limit must be a positive integer"))
            return
            
        try:
            repository = Repository(Path(""))
            matches = repository.query(query_string, limit)
            self._print_matches(matches)
            
        except FileSizeExceededError as e:
            print(Color.red(e))

        except InvalidRepositoryError as e:
            print(Color.red(e))
        
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 500:
                print(Color.red("Internal server error. Try again later or try uninitializing then initializing the current directory as an insight repository."))
            else:
                raise
