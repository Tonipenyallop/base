import unittest
from node import Node
from page import Page
from pageBuffer import PageBuffer
from fileManager import FileManager
from fileLogger import FileLogger
from clockBuffer import ClockBuffer
from mockFileManager import MockFileManager


class TestClock(unittest.TestCase):
    def testReplaceFrame(self):
        # case when frame needs to be replaced,
        # the frame pool queue should remove old Node and insert new Node to where old Node was
        file = open('testClock.txt', 'rb+')
        fileLogger = FileLogger(file)
        mockFileManager = MockFileManager(fileLogger)
        clockBuffer = ClockBuffer(mockFileManager, maxSize=3)

        # first page contains 'taesu'
        # second and third contain nothing
        # fourth page contains 'final'
        # taesu -> nothing -> nothing
        # expect page queue should be exact order of
        # final -> nothing -> nothing

        page = Page(data=bytearray(41))
        page2 = Page(data=bytearray(41))
        page3 = Page(data=bytearray(41))
        inputAsBytes = bytearray('taesu', encoding='utf-8')
        inputAsBytes2 = bytearray('final', encoding='utf-8')
        page3.write(inputAsBytes2)

        page.write(inputAsBytes)
        clockBuffer.writePage(0, page)
        self.assertEqual(mockFileManager.writeCount, 0)
        clockBuffer.writePage(1, page2)
        self.assertEqual(mockFileManager.writeCount, 0)
        clockBuffer.writePage(2, page2)
        self.assertEqual(mockFileManager.writeCount, 0)
        clockBuffer.writePage(3, page3)
        self.assertEqual(mockFileManager.writeCount, 1)
        self.assertAlmostEqual(len(clockBuffer.pinnedPagesQueue), 3)

        file.close()


if __name__ == "__main__":
    unittest.main()
