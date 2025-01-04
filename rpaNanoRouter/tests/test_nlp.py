import unittest
from rpaNanoRouter.libs.docker.nlp import Nlp

class TestNLPProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = Nlp()

    def test_stop(self):
        """
        Test the stop command.
        """
        text = "Stop container csv"
        a, b, c, d = self.processor.process_command(text)
        self.assertEqual(a, "down")
        self.assertEqual(b, "csv")

        text = "Shut down container csv"
        a, b, c, d = self.processor.process_command(text)
        self.assertEqual(a, "down")
        self.assertEqual(b, "csv")

    def test_start(self):
        """
        Test the start command.
        """
        text = "Start container csv"
        a, b, c, d = self.processor.process_command(text)
        self.assertEqual(a, "up")
        self.assertEqual(b, "csv")

        text = "Please start container csv"
        a, b, c, d = self.processor.process_command(text)
        self.assertEqual(a, "up")
        self.assertEqual(b, "csv")

        text = "Please run container csv"
        a, b, c, d = self.processor.process_command(text)
        self.assertEqual(a, "up")
        self.assertEqual(b, "csv")

    def test_show(self):
        """
        Test the show command.
        """
        text = "Show container"
        a, b, c, d = self.processor.process_command(text)
        self.assertEqual(a, "show")
        self.assertEqual(b, "container")

if __name__ == '__main__':
    unittest.main()