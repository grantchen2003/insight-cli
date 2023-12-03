from pathlib import Path

from insight_cli.commands.base.command import Command
from insight_cli.repository import Repository
from insight_cli.utils.color import Color


class UninitializeCommand(Command):
    def __init__(self):
        super().__init__(
            flags=["-u", "--uninitialize"],
            description="uninitializes the current directory as an insight repository",
        )

    def execute(self) -> None:
        repository = Repository(Path.cwd())

        try:
            repository.uninitialize()
            print(Color.green("The current insight repository has been uninitialized."))

        except FileNotFoundError:
            print(Color.red("The current directory is not an insight repository."))
