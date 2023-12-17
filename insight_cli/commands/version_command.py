from .base.command import Command
from insight_cli.config import config


class VersionCommand(Command):
    def __init__(self):
        super().__init__(
            flags=["-v", "--version"],
            description="shows the current version of insight",
        )

    def execute(self) -> None:
        print(f"insight-cli v{config.INSIGHT_VERSION}")
