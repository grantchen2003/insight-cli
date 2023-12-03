import unittest

from insight_cli.utils import Color


class TestColor(unittest.TestCase):
    def test_red(self):
        text = "Test in red"
        colored_text = Color.red(text)
        expected_output = f"\033[91m{text}\033[0m"
        self.assertEqual(colored_text, expected_output)

    def test_green(self):
        text = "Test in green"
        colored_text = Color.green(text)
        expected_output = f"\033[92m{text}\033[0m"
        self.assertEqual(colored_text, expected_output)

    def test_yellow(self):
        text = "Test in yellow"
        colored_text = Color.yellow(text)
        expected_output = f"\033[93m{text}\033[0m"
        self.assertEqual(colored_text, expected_output)


if __name__ == "__main__":
    unittest.main()
