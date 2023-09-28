import unittest
from node import Node
from page import Page
from pageBuffer import PageBuffer
from fileManager import FileManager
from fileLogger import FileLogger
from clockBuffer import ClockBuffer


class TestClock(unittest.TestCase):
    def testReplaceFrame(self):
        # case when frame needs to be replaced,
        # the frame pool queue should remove old Node and insert new Node to where old Node was
        file = open('testClock.txt', 'rb+')
        fileLogger = FileLogger(file)
        fileManager = FileManager(fileLogger)
        clockBuffer = ClockBuffer(fileManager, maxSize=3)

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
        clockBuffer.writePage(1, page2)
        clockBuffer.writePage(2, page2)
        clockBuffer.writePage(3, page3)
        # print("page.data")
        # print(page.data)

        self.assertAlmostEqual(len(clockBuffer.pinnedPagesQueue), 3)
        # print('inputAsBytes')
        # print(inputAsBytes)
        # print("page.data")
        # print(page.data)
        # framePool = [
        #     Node(0, Page(bytearray('first', encoding='utf-8'))),
        #     Node(1, Page(bytearray('secon', encoding='utf-8'))),
        #     Node(2, Page(bytearray('third', encoding='utf-8'))),
        #     Node(3, Page(bytearray('fourt', encoding='utf-8')))
        # ]

        file.close()
        # fileLogger = FileLogger(file)
        # fileManager = FileManager(fileLogger)
        # pageBuffer = PageBuffer(fileManager)
        # result = pageBuffer.clock.replaceFrame(
        #     4, Page(bytearray('fifth', encoding='utf-8')), framePool)
        # self.assertEqual(result, -1)

    # def testReplaceFrameFull(self):
    #     framePool = [
    #         Node(0, Page(bytearray('first', encoding='utf-8'))),
    #         Node(1, Page(bytearray('secon', encoding='utf-8'))),
    #         Node(2, Page(bytearray('third', encoding='utf-8'))),
    #         Node(3, Page(bytearray('fourt', encoding='utf-8'))),
    #         Node(4, Page(bytearray('fifth', encoding='utf-8'))),
    #         Node(5, Page(bytearray('sixth', encoding='utf-8'))),
    #     ]
    #     file = open('testClock.txt', 'rb+')
    #     file.close()
    #     fileLogger = FileLogger(file)
    #     fileManager = FileManager(fileLogger)
    #     pageBuffer = PageBuffer(fileManager)
    #     result = pageBuffer.clock.replaceFrame(
    #         6, Page(bytearray('seven', encoding='utf-8')), framePool)

    #     # 1. check correct clock hand value is returned
    #     self.assertEqual(result, 0)

    #     prevClockHand = pageBuffer.clock.clockHand - 1

    #     # 2. check framePool is updated properly
    #     self.assertEqual(framePool[prevClockHand].page.data, bytearray(
    #         'seven', encoding='utf-8'))

    #     result2 = pageBuffer.clock.replaceFrame(
    #         7, Page(bytearray('eight', encoding='utf-8')), framePool)
    #     self.assertEqual(result2, 1)

    #     prevClockHand = pageBuffer.clock.clockHand - 1

    #     self.assertEqual(framePool[prevClockHand].page.data, bytearray(
    #         'eight', encoding='utf-8'))

    #     result3 = pageBuffer.clock.replaceFrame(
    #         8, Page(bytearray('ninet', encoding='utf-8')), framePool)
    #     self.assertEqual(result3, 2)

    # def testReplaceFrameContainPage(self):
    #     framePool = [
    #         Node(0, Page(bytearray('first', encoding='utf-8'))),
    #         Node(1, Page(bytearray('secon', encoding='utf-8'))),
    #         Node(2, Page(bytearray('third', encoding='utf-8'))),
    #         Node(3, Page(bytearray('fourt', encoding='utf-8'))),
    #         Node(4, Page(bytearray('fifth', encoding='utf-8'))),
    #         Node(5, Page(bytearray('sixth', encoding='utf-8'))),
    #     ]
    #     file = open('testClock.txt', 'rb+')
    #     file.close()
    #     fileLogger = FileLogger(file)
    #     fileManager = FileManager(fileLogger)
    #     pageBuffer = PageBuffer(fileManager)

    #     result = pageBuffer.clock.replaceFrame(
    #         3, Page(bytearray('fourt', encoding='utf-8')), framePool)
    #     self.assertEqual(result, -1)

    # # the case if framePool has available space and called with unpinned node page
    # # expect -> framePool adds input node page
    # def testReplaceFrameUpdateFramePool(self):
    #     framePool = [
    #         Node(0, Page(bytearray('first', encoding='utf-8'))),
    #         Node(1, Page(bytearray('secon', encoding='utf-8'))),
    #         Node(2, Page(bytearray('third', encoding='utf-8'))),
    #     ]
    #     file = open('testClock.txt', 'rb+')
    #     file.close()
    #     fileLogger = FileLogger(file)
    #     fileManager = FileManager(fileLogger)
    #     pageBuffer = PageBuffer(fileManager)

    #     result = pageBuffer.clock.replaceFrame(
    #         3, Page(bytearray('fourt', encoding='utf-8')), framePool)

    #     self.assertEqual(result, -1)
    #     self.assertEqual(framePool[-1].page.data.decode(), "fourt")


if __name__ == "__main__":
    unittest.main()
