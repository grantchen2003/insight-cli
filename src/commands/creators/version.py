import yaml

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
    with open("insight.yaml", "r") as file:
        config = yaml.safe_load(file)
        
    print(Color.green(f"insight-cli v{config["version"]}"))


