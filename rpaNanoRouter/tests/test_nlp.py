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
        dt = self.processor.process_command(text)
        self.assertEqual(dt['command'], "down")
        self.assertEqual(dt['target'], "csv")

        text = "Shut down container csv"
        dt = self.processor.process_command(text)
        self.assertEqual(dt['command'], "down")
        self.assertEqual(dt['target'], "csv")

    def test_start(self):
        """
        Test the start command.
        """
        text = "Start container csv"
        dt = self.processor.process_command(text)
        self.assertEqual(dt['command'], "up")
        self.assertEqual(dt['target'], "csv")

        text = "Please start container csv"
        dt = self.processor.process_command(text)
        self.assertEqual(dt['command'], "up")
        self.assertEqual(dt['target'], "csv")

        text = "Please run container csv"
        dt = self.processor.process_command(text)
        self.assertEqual(dt['command'], "up")
        self.assertEqual(dt['target'], "csv")

    def test_show(self):
        """
        Test the show command.
        """
        text = "Show container"
        dt = self.processor.process_command(text)
        self.assertEqual(dt['command'], "show")
        self.assertEqual(dt['target'], "container")
        
        text = "list me container"
        dt = self.processor.process_command(text)
        self.assertEqual(dt['command'], "show")
        self.assertEqual(dt['target'], "container")
        
        text = "show all running containers"
        dt = self.processor.process_command(text)
        self.assertEqual(dt['command'], "show")
        self.assertEqual(dt['target'], "container")
        self.assertTrue('active' in dt['related_tokens'] or 'run' in dt['related_tokens'])
        
        text = "show exited containers"
        dt = self.processor.process_command(text)
        self.assertEqual(dt['command'], "show")
        self.assertEqual(dt['target'], "container")
        self.assertTrue('inactive' in dt['related_tokens'] or 'exit' in dt['related_tokens'])
        
        text = "list me volumes"
        dt = self.processor.process_command(text)
        self.assertEqual(dt['command'], "show")
        self.assertEqual(dt['target'], "volume")
        
        text = "obtain all the images"
        dt = self.processor.process_command(text)
        self.assertEqual(dt['command'], "show")
        self.assertEqual(dt['target'], "image")
        
        text = "please fetch the images for me"
        dt = self.processor.process_command(text)
        self.assertEqual(dt['command'], "show")
        self.assertEqual(dt['target'], "image")

    def test_copy(self):
        """
        Test the copy command.
        """
        text = "please transfer file test.txt into container git in /home"
        dt = self.processor.process_command(text)
        self.assertEqual(dt['command'], "copy")
        self.assertEqual(dt['target'], "git")
        self.assertEqual(dt['related_tokens'], ['container'])
        self.assertEqual(dt['source'], 'test.txt')
        self.assertEqual(dt['path'], '/home')
        
        text = "please transfer file test.txt into container git in /home/data/db/mysql"
        dt = self.processor.process_command(text)
        self.assertEqual(dt['command'], "copy")
        self.assertEqual(dt['target'], "git")
        self.assertEqual(dt['related_tokens'], ['container', 'in'])
        self.assertEqual(dt['source'], 'test.txt')
        self.assertEqual(dt['path'], '/home/data/db/mysql')
        
        text = "please transfer file at src/data/test.txt into container git in /home"
        dt = self.processor.process_command(text)
        self.assertEqual(dt['command'], "copy")
        self.assertEqual(dt['target'], "git")
        self.assertEqual(dt['related_tokens'], ['container'])
        self.assertEqual(dt['source'], 'src/data/test.txt')
        self.assertEqual(dt['path'], '/home')

if __name__ == '__main__':
    unittest.main()