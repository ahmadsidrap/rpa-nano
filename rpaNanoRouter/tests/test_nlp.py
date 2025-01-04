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
        
        text = "list me container"
        a, b, c, d = self.processor.process_command(text)
        self.assertEqual(a, "show")
        self.assertEqual(b, "container")
        
        text = "show all running containers"
        a, b, c, d = self.processor.process_command(text)
        self.assertEqual(a, "show")
        self.assertEqual(b, "container")
        self.assertTrue('active' in c or 'run' in c)
        
        text = "show all exited containers"
        a, b, c, d = self.processor.process_command(text)
        self.assertEqual(a, "show")
        self.assertEqual(b, "container")
        self.assertTrue('inactive' in c or 'exit' in c)
        
        text = "list me volumes"
        a, b, c, d = self.processor.process_command(text)
        self.assertEqual(a, "show")
        self.assertEqual(b, "volume")
        
        text = "obtain all the images"
        a, b, c, d = self.processor.process_command(text)
        self.assertEqual(a, "show")
        self.assertEqual(b, "image")
        
        text = "please fetch the images for me"
        a, b, c, d = self.processor.process_command(text)
        self.assertEqual(a, "show")
        self.assertEqual(b, "image")

    def test_copy(self):
        """
        Test the copy command.
        """
        text = "please transfer file test.txt into container git in /home"
        a, b, c, d = self.processor.process_command(text)
        self.assertEqual(a, "copy")
        self.assertEqual(b, "git")
        self.assertEqual(c, ['container'])
        self.assertEqual(d['source'], 'test.txt')
        self.assertEqual(d['path'], '/home')
        
        text = "please transfer file test.txt into container git in /home/data/db/mysql"
        a, b, c, d = self.processor.process_command(text)
        self.assertEqual(a, "copy")
        self.assertEqual(b, "git")
        self.assertEqual(c, ['container', 'in'])
        self.assertEqual(d['source'], 'test.txt')
        self.assertEqual(d['path'], '/home/data/db/mysql')
        
        text = "please transfer file at src/data/test.txt into container git in /home"
        a, b, c, d = self.processor.process_command(text)
        self.assertEqual(a, "copy")
        self.assertEqual(b, "git")
        self.assertEqual(c, ['container'])
        self.assertEqual(d['source'], 'src/data/test.txt')
        self.assertEqual(d['path'], '/home')

if __name__ == '__main__':
    unittest.main()