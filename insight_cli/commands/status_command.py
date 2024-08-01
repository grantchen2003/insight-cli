from pathlib import Path

from .base.command import Command
from insight_cli.repository import Repository
from insight_cli.utils import Color


class StatusCommand(Command):
    def __init__(self):
        super().__init__(
            flags=["-s", "--status"],
            description="displays the insight repository status of the current directory",
        )

    def execute(self) -> None:
        repository = Repository(Path(""))

        if not repository.is_valid:
            terminal_output = f"{repository.path.resolve()} is not a valid insight repository"

            print(Color.red(terminal_output))

        else:
            terminal_output = f"{repository.path.resolve()} is a valid insight repository"

            print(Color.green(terminal_output))
