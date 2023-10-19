import unittest
from main import readPages
from mockFile import MockFile
from clockBuffer import ClockBuffer
from mockPageAccessor import MockPageAccessor

wordLength = 5
bitmapLength = 1
bitmapSize = 8

pageLength = wordLength * bitmapSize + bitmapLength


class TestMain(unittest.TestCase):
    # case when user wrote 3 pages and restart program
    def testReadPages(self):
        fakeFile = MockFile(returnValue=123)
        # fake file length is 123
        [unfilledPageIndexes, maxPageIndex] = readPages(
            fakeFile, pageLength, MockPageAccessor)
        self.assertEqual(len(unfilledPageIndexes), 3)


if __name__ == '__main__':
    unittest.main()
