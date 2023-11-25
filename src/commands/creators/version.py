from src.commands.classes import Command
from src.utils.color import Color


def create_version_command() -> Command:
    return Command(
        flags=["-v", "--version"],
        description="shows the current version of insight",
        handler={
            "params": [],
            "function": handle_version_command,
        },
    )


def handle_version_command() -> None:
    print(Color.green("insight-cli v0.0.0"))
