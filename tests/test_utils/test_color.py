import unittest

from insight_cli.utils import Color


class TestColor(unittest.TestCase):
    def test_red_with_empty_text(self):
        text = ""
        expected_output = f"\033[91m{text}\033[0m"
        self.assertEqual(Color.red(text), expected_output)

    def test_red_with_non_empty_text(self):
        text = "Test in red"
        expected_output = f"\033[91m{text}\033[0m"
        self.assertEqual(Color.red(text), expected_output)

    def test_green_with_empty_text(self):
        text = ""
        expected_output = f"\033[92m{text}\033[0m"
        self.assertEqual(Color.green(text), expected_output)

    def test_green_with_non_empty_text(self):
        text = "Test in green"
        expected_output = f"\033[92m{text}\033[0m"
        self.assertEqual(Color.green(text), expected_output)

    def test_yellow_with_empty_text(self):
        text = ""
        expected_output = f"\033[93m{text}\033[0m"
        self.assertEqual(Color.yellow(text), expected_output)

    def test_yellow_with_non_empty_text(self):
        text = "Test in yellow"
        expected_output = f"\033[93m{text}\033[0m"
        self.assertEqual(Color.yellow(text), expected_output)


if __name__ == "__main__":
    unittest.main()
