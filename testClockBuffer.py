import unittest
from clockBuffer import ClockBuffer
from fileManager import FileManager
from fileLogger import FileLogger
from page import Page


class TestClockBuffer(unittest.TestCase):
    def testGetPage(self):
        file = open('testPageBuffer.txt', 'rb+')
        fileLogger = FileLogger(file)
        fileManager = FileManager(fileLogger)
        clockBuffer = ClockBuffer(fileManager)
        # 1. case pageIndex stored in pagePool
        fakePageObject = {'_id': 'fakePageId'}
        clockBuffer.pagePool[1] = fakePageObject
        result = clockBuffer.getPage(1)
        self.assertEqual(result['_id'], 'fakePageId')
        file.close()

    def testWritePage(self):
        file = open('testPageBuffer.txt', 'rb+')
        fileLogger = FileLogger(file)
        fileManager = FileManager(fileLogger)
        clockBuffer = ClockBuffer(fileManager, maxSize=3)

        page = Page(data=bytearray(41))

        page.write(b'firstdragonthirdsquidhello')
        # 2. case frame needs to be replaced due to max size
        clockBuffer.writePage(0, page)
        clockBuffer.writePage(1, page)
        clockBuffer.writePage(2, page)
        clockBuffer.writePage(3, page)
        assert len(clockBuffer.pagePool.keys()) == 3

        file.close()


if __name__ == '__main__':
    unittest.main()
