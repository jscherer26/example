import sys
import unittest
import logging

from src.progressbar import ProgressBar

class SetDatabaseTestCase(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger()
        self.logger.level = logging.DEBUG
        self.logger.addHandler(logging.StreamHandler(sys.stdout))
        self.pb = ProgressBar()
    def tearDown(self):
        self.logger = None
        self.pb = None
    def test__add__(self):
        self.assertEqual(self.pb.__str__(), '[>............] 0%')
        self.pb = self.pb + 5
        self.assertEqual(self.pb.__str__(), '[======>......] 50%')
        self.pb = self.pb + 5
        self.assertEqual(self.pb.__str__(), '[============>] 100%')
    def test__str__(self):
        self.assertEqual(self.pb.__str__(), '[>............] 0%')
        self.pb.progress = 30
        self.pb.width = 12
        self.pb.step = 100 / float(self.pb.width)
        self.pb.fill = "-"
        self.pb.blank = "."
        self.assertEqual(self.pb.__str__(), '[--->.........] 30%')
    def test_get_progress(self):
        self.pb.end = 10
        self.assertEqual(self.pb._get_progress(1), 10.0)
        self.pb.end = 50
        self.assertEqual(self.pb._get_progress(10), 20.0)
    def test_get_progress(self):
        self.pb.end = 10
        self.assertEqual(self.pb._get_progress(1), 10.0)
        self.pb.end = 50
        self.assertEqual(self.pb._get_progress(10), 20.0)
