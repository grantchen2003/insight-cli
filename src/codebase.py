import insight_dir
import insightignore_file
import json
import os
from pathlib import Path
import requests
import utils
from utils import Directory


def initialize(codebase_dir_path: Path) -> None:
    insight_dir_path: Path = codebase_dir_path / "insight"

    if insight_dir.is_valid(insight_dir_path):
        reinitialize(codebase_dir_path)
        return

    # read .insightignore file
    insightignore_file_path: Path = codebase_dir_path / ".insightignore"
    ignorable_names: list[str] = insightignore_file.get_ignorable_names(
        insightignore_file_path
    )

    # get all dirs/files in codebase excluding those in .insightignore
    codebase_dir: Directory = utils.create_directory_from_path(
        dir_path=codebase_dir_path, ignorable_names=ignorable_names
    )

    try:
        # send to codebase to server
        response = requests.post(
            url=os.environ.get("API_GATEWAY_URL"),
            json=json.dumps(codebase_dir.to_dict(), default=str),
        )
        response_data = response.json()
        response_data = json.loads(response_data["json"])
        print(json.dumps(response_data, indent=2))

    except requests.exceptions.RequestException as e:
        # Handle any request-related exceptions
        print("Error making the request:", e)

    except json.JSONDecodeError as e:
        # Handle JSON decoding error
        print("Error decoding JSON response:", e)

    # create .insight directory


# raises Exception if [insight_dir_path] is an invalid .insight dir path
def reinitialize(codebase_dir_path: Path) -> None:
    insight_dir_path: Path = codebase_dir_path / "insight"

    if not insight_dir.is_valid(insight_dir_path):
        raise insight_dir.InvalidInsightDirectoryPathError(insight_dir_path)
    # TODO


def uninitialize(codebase_dir_path: Path) -> None:
    print("uninitialize")
