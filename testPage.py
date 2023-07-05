import unittest

from page import Page


class TestPage(unittest.TestCase):
    def testRead(self):
        newPage = Page([0b00000010, 21, 57, 192, 30, 239, 10, 20, 30, 40, 50])
        self.assertEqual(newPage.read(0), None)

        expect = [10, 20, 30, 40, 50]
        self.assertEqual(newPage.read(1), expect)

    def testDeleted(self):
        expect = [21, 57, 192, 30, 239]
        newPage = Page([0b00000011, 21, 57, 192, 30, 239, 0, 0, 0, 0, 0])

        self.assertEqual(newPage.read(0), expect)
        newPage.delete(0)
        self.assertEqual(newPage.read(0), None)

    def testWrite(self):
        # case 1 return to idx where inserted, insert to available empty space
        newPage = Page([0b00000000])
        expected = [11, 12, 13, 14, 15]

        self.assertEqual(newPage.write(expected), 0)

    # case 1 return to idx where inserted, insert to available empty space
        newPage = Page([0b00000010, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2])
        expected = [11, 12, 13, 14, 15]

        self.assertEqual(newPage.write(expected), 0)
        self.assertEqual(newPage.data[0], 0b00000011)
        self.assertEqual(newPage.read(0), expected)

    # case 2. no available emtpy space
        newPage = Page([0b11111111, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5,
                        1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5])
        self.assertEqual(newPage.write([1, 2, 3, 4, 5]), -1)


if __name__ == '__main__':
    unittest.main()
