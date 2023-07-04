import unittest

from page import Page


class TestPage(unittest.TestCase):
    def testRead(self):
        expect = [0, 0, 0, 0, 0]
        newPage = Page(0b00000010)
        newPage.data = [0b00000010, 21, 57, 192, 30, 239, 0, 0, 0, 0, 0]
        self.assertEqual(newPage.read(0), None)

        self.assertEqual(newPage.read(1), expect)

    def testDeleted(self):
        expect = [21, 57, 192, 30, 239]
        newPage = Page(0b00000011)
        newPage.data = [0b00000011, 21, 57, 192, 30, 239, 0, 0, 0, 0, 0]

        self.assertEqual(newPage.read(0), expect)
        newPage.delete(0)
        self.assertEqual(newPage.read(0), None)


if __name__ == '__main__':
    unittest.main()
