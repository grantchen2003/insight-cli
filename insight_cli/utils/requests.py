from typing import Any, Callable

import requests


def handle_make_request_exceptions(make_request: Callable) -> Callable:
    def wrapper(*args, **kwargs) -> Any:
        try:
            return make_request(*args, **kwargs)

        except requests.exceptions.ConnectionError as e:
            return {"error_message": f"Connection error occurred: {e}"}

        except requests.exceptions.Timeout as e:
            return {"error_message": f"Request timed out: {e}"}

        except requests.exceptions.HTTPError as e:
            return {"error_message": f"HTTP error: {e}"}

        except requests.exceptions.RequestException as e:
            return {"error_message": f"General request exception: {e}"}

        except ValueError as e:
            return {"error_message": f"Failed to parse JSON: {e}"}

        except Exception as e:
            return {"error_message": e}

    return wrapper
