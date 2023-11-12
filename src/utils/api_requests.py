from .directory import Directory
import json
import os
import requests


def initialize_codebase(codebase_dir: Directory) -> dict[str, str]:
    # try:
    request_url = f"{os.environ.get('API_BASE_URL')}/initialize_codebase"
    request_json_body = json.dumps(
        {"codebase": codebase_dir.to_dict()},
        default=str,
    )
    response = requests.post(url=request_url, json=request_json_body)
    # check that the request was successful (status code 2xx)
    response.raise_for_status()
    return response.json()

    # except requests.exceptions.ConnectionError as e:
    #     return {"error_message": f"Connection error occurred: {e}"}

    # except requests.exceptions.Timeout as e:
    #     return {"error_message": f"Request timed out: {e}"}

    # except requests.exceptions.HTTPError as e:
    #     return {"error_message": f"HTTP error: {e}"}

    # except requests.exceptions.RequestException as e:
    #     return {"error_message": f"General request exception: {e}"}

    # except ValueError as e:
    #     return {"error_message": f"Failed to parse JSON: {e}"}

    # except Exception as e:
    #     return {"error_message": e}
