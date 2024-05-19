from pathlib import Path

from .base.command import Command
from insight_cli.repository import Repository, InvalidRepositoryError
from insight_cli.utils import Color


class UninitializeCommand(Command):
    def __init__(self):
        super().__init__(
            flags=["-u", "--uninitialize"],
            description="uninitializes the current directory as an insight repository",
        )

    def execute(self) -> None:
        try:
            repository = Repository(Path(""))

            repository.uninitialize()

            terminal_output = (
                f"Uninitialized insight repository in {repository.path.resolve()}"
            )

            print(Color.green(terminal_output))

        except InvalidRepositoryError as e:
            print(Color.red(e))
