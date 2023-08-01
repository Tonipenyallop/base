import unittest
from node import Node
from page import Page
from pageBuffer import PageBuffer
from fileManager import FileManager
from fileLogger import FileLogger


class TestClock(unittest.TestCase):
    def testReplaceFrameNotFull(self):
        framePool = [
            Node(0, Page(bytearray('first', encoding='utf-8'))),
            Node(1, Page(bytearray('secon', encoding='utf-8'))),
            Node(2, Page(bytearray('third', encoding='utf-8'))),
            Node(3, Page(bytearray('fourt', encoding='utf-8')))
        ]
        file = open('testClock.txt', 'rb+')
        file.close()
        fileLogger = FileLogger(file)
        fileManager = FileManager(fileLogger)
        pageBuffer = PageBuffer(fileManager)
        result = pageBuffer.clock.replaceFrame(
            4, Page(bytearray('fifth', encoding='utf-8')), framePool)
        self.assertEqual(result, -1)

    def testReplaceFrameFull(self):
        framePool = [
            Node(0, Page(bytearray('first', encoding='utf-8'))),
            Node(1, Page(bytearray('secon', encoding='utf-8'))),
            Node(2, Page(bytearray('third', encoding='utf-8'))),
            Node(3, Page(bytearray('fourt', encoding='utf-8'))),
            Node(4, Page(bytearray('fifth', encoding='utf-8'))),
            Node(5, Page(bytearray('sixth', encoding='utf-8'))),
        ]
        file = open('testClock.txt', 'rb+')
        file.close()
        fileLogger = FileLogger(file)
        fileManager = FileManager(fileLogger)
        pageBuffer = PageBuffer(fileManager)
        result = pageBuffer.clock.replaceFrame(
            6, Page(bytearray('seven', encoding='utf-8')), framePool)

        # 1. check correct clock hand value is returned
        self.assertEqual(result, 0)

        prevClockHand = pageBuffer.clock.clockHand - 1

        # 2. check framePool is updated properly
        self.assertEqual(framePool[prevClockHand].page.data, bytearray(
            'seven', encoding='utf-8'))

        result2 = pageBuffer.clock.replaceFrame(
            7, Page(bytearray('eight', encoding='utf-8')), framePool)
        self.assertEqual(result2, 1)

        prevClockHand = pageBuffer.clock.clockHand - 1

        self.assertEqual(framePool[prevClockHand].page.data, bytearray(
            'eight', encoding='utf-8'))

        result3 = pageBuffer.clock.replaceFrame(
            8, Page(bytearray('ninet', encoding='utf-8')), framePool)
        self.assertEqual(result3, 2)

    def testReplaceFrameContainPage(self):
        framePool = [
            Node(0, Page(bytearray('first', encoding='utf-8'))),
            Node(1, Page(bytearray('secon', encoding='utf-8'))),
            Node(2, Page(bytearray('third', encoding='utf-8'))),
            Node(3, Page(bytearray('fourt', encoding='utf-8'))),
            Node(4, Page(bytearray('fifth', encoding='utf-8'))),
            Node(5, Page(bytearray('sixth', encoding='utf-8'))),
        ]
        file = open('testClock.txt', 'rb+')
        file.close()
        fileLogger = FileLogger(file)
        fileManager = FileManager(fileLogger)
        pageBuffer = PageBuffer(fileManager)

        result = pageBuffer.clock.replaceFrame(
            3, Page(bytearray('fourt', encoding='utf-8')), framePool)
        self.assertEqual(result, -1)

    # the case if framePool has available space and called with unpinned node page
    # expect -> framePool adds input node page
    def testReplaceFrameUpdateFramePool(self):
        framePool = [
            Node(0, Page(bytearray('first', encoding='utf-8'))),
            Node(1, Page(bytearray('secon', encoding='utf-8'))),
            Node(2, Page(bytearray('third', encoding='utf-8'))),
        ]
        file = open('testClock.txt', 'rb+')
        file.close()
        fileLogger = FileLogger(file)
        fileManager = FileManager(fileLogger)
        pageBuffer = PageBuffer(fileManager)

        result = pageBuffer.clock.replaceFrame(
            3, Page(bytearray('fourt', encoding='utf-8')), framePool)

        self.assertEqual(result, -1)
        self.assertEqual(framePool[-1].page.data.decode(), "fourt")


if __name__ == "__main__":
    unittest.main()
