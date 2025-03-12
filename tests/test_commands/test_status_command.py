# from pathlib import Path
# from unittest.mock import patch
# import unittest

# from insight_cli.commands import StatusCommand
# from insight_cli.utils import Color


# class TestStatusCommand(unittest.TestCase):
#     @patch("builtins.print")
#     @patch("insight_cli.api.ValidateRepositoryIdAPI.make_request")
#     def test_execute_with_valid_repository(
#         self, mock_validate_repository_id_api_make_request, mock_print
#     ) -> None:
#         status_command = StatusCommand()

#         mock_validate_repository_id_api_make_request.return_value = {
#             "repository_id_is_valid": True
#         }

#         status_command.execute()

#         mock_validate_repository_id_api_make_request.assert_called_once()
#         mock_print.assert_called_once_with(
#             Color.green(f"{Path.cwd()} is a valid repository")
#         )


# if __name__ == "__main__":
#     unittest.main()
