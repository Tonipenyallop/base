import unittest
import os
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

    def testGetPage2(self):
        # the case when user restart program which previous data was 3 pages stored
        # todo taesu this is the problem
        # it means we don't know this page
        # if pool is not full, update local page pool

        # todo 1. re-running
        # todo 2. 'original' testcase which means commit save version of 'testcase.txt' file

        # 1.case if the page was empty and read was called

        # 2.case page index was not stored in local data
        # And not in db
        #  -> check db -> yes or no
        pass

    def testWritePage(self):
        file = open('testPageBuffer.txt', 'rb+')
        fileLogger = FileLogger(file)
        fileManager = FileManager(fileLogger)
        clockBuffer = ClockBuffer(fileManager, maxSize=3)

        page = Page(data=bytearray(41))
        page.write(b'firstdragonthirdsquidhello')

        page2 = Page(data=bytearray(41))
        page2.write(b'ThisIsPage2NeedsToBeSecond')

        # 2. case frame needs to be replaced due to max size
        clockBuffer.writePage(0, page)
        clockBuffer.writePage(1, page)
        clockBuffer.writePage(2, page)
        clockBuffer.writePage(3, page2)
        assert len(clockBuffer.pagePool.keys()) == 3

        file.close()

    def testEvictionAndReadback(self):
        # When the pool is full and a new page is requested, the buffer must
        # evict via CLOCK, flush the dirty victim to disk, and still serve the
        # evicted page correctly on a later access -- without crashing.
        path = 'testEvict.bin'
        open(path, 'wb').close()
        file = open(path, 'rb+')
        clockBuffer = ClockBuffer(FileManager(FileLogger(file)), maxSize=2)

        pageA = Page(data=bytearray(41))
        pageA.write(b'aaaaa')
        pageB = Page(data=bytearray(41))
        pageB.write(b'bbbbb')
        pageC = Page(data=bytearray(41))
        pageC.write(b'ccccc')

        clockBuffer.writePage(0, pageA)
        clockBuffer.writePage(1, pageB)
        clockBuffer.writePage(2, pageC)  # pool full -> evicts + flushes a page

        self.assertEqual(len(clockBuffer.pagePool.keys()), 2)
        self.assertEqual(len(clockBuffer.pinnedPagesQueue), 2)

        # the evicted page must be re-readable from disk with its real contents
        self.assertEqual(clockBuffer.getPage(0).read(0), b'aaaaa')
        self.assertEqual(clockBuffer.getPage(2).read(0), b'ccccc')

        file.close()
        os.remove(path)


if __name__ == '__main__':
    unittest.main()
