from io import FileIO
from page import Page
wordLength = 5
bitmapLength = 1
bitmapSize = 8


class FileManager:
    def __init__(self, file: FileIO) -> None:
        self.file = file
        self.wordLength = 5
        self.bitmapLength = 1
        self.bitmapSize = 8
        self.pageLength = self.wordLength * self.bitmapSize + self.bitmapLength

    def getPage(self, pageIndex) -> Page:
        startPageIndex = pageIndex * self.pageLength
        self.file.seek(startPageIndex)
        # 1. get the whole page with page index
        data = bytearray(self.file.read(self.pageLength + self.bitmapLength))

        # 2. fill out with zero if page is not filled
        numberOfZero = self.pageLength - len(data)
        data.extend([0]*numberOfZero)
        page = Page(data, wordLength,
                    bitmapLength, bitmapSize)
        return page

    def writePage(self, index: int, page: Page) -> None:
        startPageIndex = index * self.pageLength
        self.file.seek(startPageIndex)
        self.file.write(page.data)
