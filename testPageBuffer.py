import unittest

from fileLogger import FileLogger
from fileManager import FileManager
from pageBuffer import PageBuffer
from page import Page


class TestPageBuffer(unittest.TestCase):
    # def testWritePage(self):
    #     file = open('testPageBuffer.txt', 'rb+')
    #     file.close()
    #     fileLogger = FileLogger(file)
    #     fileManager = FileManager(fileLogger)
    #     pageBuffer = PageBuffer(fileManager)

    #     pageBuffer.writePage(0, Page(bytearray('first', encoding='utf-8')))
    #     result = pageBuffer.writePage(
    #         0, Page(bytearray('second', encoding='utf-8')))

    #     # 1. check if page is stored in currentPineddPages, skip writing
    #     self.assertEqual(result, None)

    #     fileReadCounts = pageBuffer.fileManager.fileLogger.close()
    #     # 2. check if reading files are all 0s
    #     self.assertEqual(
    #         fileReadCounts, "self.readCount:0, self.seekCount:0, self.writeCount:0")

    #     # pageBuffer.writePage(0, Page(bytearray(
    #     #     "b'\xff'happyhappyhappyhappyhappyhappyhappyhappy", encoding='utf-8')))
    #     # pageBuffer.writePage(0, Page(bytearray('happy', encoding='utf-8')))
    #     # pageBuffer.writePage(0, Page(bytearray('happy', encoding='utf-8')))
    #     # pageBuffer.writePage(0, Page(bytearray('happy', encoding='utf-8')))
    #     # pageBuffer.writePage(0, Page(bytearray('happy', encoding='utf-8')))
    #     # pageBuffer.writePage(0, Page(bytearray('happy', encoding='utf-8')))
    #     # pageBuffer.writePage(0, Page(bytearray('happy', encoding='utf-8')))
    #     # print(b'\x7f'.decode())
    #     # print((255).to_bytes(1, 'big'))
    #     # pageBuffer.writePage(2, Page(bytearray('lmfao', encoding='utf-8')))
    #     # pageBuffer.writePage(3, Page(bytearray('taesu', encoding='utf-8')))
    #     # pageBuffer.writePage(4, Page(bytearray('tonio', encoding='utf-8')))
    #     # pageBuffer.writePage(5, Page(bytearray('drago', encoding='utf-8')))
    #     # # 3. should be replaced
    #     # pageBuffer.writePage(6, Page(bytearray('final', encoding='utf-8')))

    def testWritePageReplace(self):
        file = open('testPageBuffer.txt', 'rb+')
        fileLogger = FileLogger(file)
        fileManager = FileManager(fileLogger)
        pageBuffer = PageBuffer(fileManager)

        pageBuffer.currentPageIndex = 0
        pageBuffer.currentPage = Page(bytearray(
            '\x7fthirdafterafterafterafterafterafterhappy', encoding='utf-8'))
        pageBuffer.flush()

        pageBuffer.currentPageIndex = 1
        pageBuffer.currentPage = Page(bytearray(
            '\x7fthirdafterafterafterafterafterafterhappy', encoding='utf-8'))
        pageBuffer.flush()

        pageBuffer.currentPageIndex = 2
        pageBuffer.currentPage = Page(bytearray(
            '\x7fthirdafterafterafterafterafterafterhappy', encoding='utf-8'))
        pageBuffer.flush()

        pageBuffer.currentPageIndex = 3
        pageBuffer.currentPage = Page(bytearray(
            '\x7fthirdafterafterafterafterafterafterhappy', encoding='utf-8'))
        pageBuffer.flush()

        pageBuffer.currentPageIndex = 4
        pageBuffer.currentPage = Page(bytearray(
            '\x7fthirdafterafterafterafterafterafterhappy', encoding='utf-8'))
        pageBuffer.flush()

        pageBuffer.currentPageIndex = 5
        pageBuffer.currentPage = Page(bytearray(
            '\x7fthirdafterafterafterafterafterafterhappy', encoding='utf-8'))
        pageBuffer.flush()

        # should be replaced
        result = pageBuffer.writePage(6, Page(bytearray(
            'b\xfffinalfinalfinalfinalfinalfinalfinalfinal', encoding='utf-8')))

        file.close()
        print("result")
        print(result)
        tmp = (255).to_bytes(1, 'big')
        print(tmp)
        # print(tmp)

        # print((255).to_bytes(1, 'big'))


if __name__ == '__main__':
    unittest.main()
