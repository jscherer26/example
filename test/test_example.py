import unittest

class TestExample(unittest.TestCase):

    def setUp(self):
        self.colors = ['red', 'blue', 'orange']
    
    def tearDown(self):
        pass

    def testAssertEqual(self):
        self.assertEqual(1, 1)

    def testAssertTrue(self):
        self.assertTrue(self.colors[1] == self.colors[1])

    def testAssertFalse(self):
        self.assertFalse(self.colors[0] == self.colors[1])

# Run test
if __name__ == "__main__":
    unittest.main()
