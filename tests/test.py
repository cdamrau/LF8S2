import unittest

class MyTestCase(unittest.TestCase):
    def test_example(self):
        self.assertEqual(2 + 2, 4)

if __name__ == '__main__':
    unittest.main()