from fileManager import FileManager
from page import Page


class PageBuffer:
    def __init__(self, fileManager: FileManager) -> None:
        self.fileManager = fileManager
        self.currentPageIndex = None
        self.currentPage = None
        self.isDirty = False

    def getPage(self, pageIndex) -> Page:
        if (self.currentPageIndex == pageIndex):
            return self.currentPage
        self.currentPageIndex = pageIndex
        self.currentPage = self.fileManager.getPage(pageIndex)
        return self.currentPage

    def writePage(self, index: int, page: Page) -> None:
        # 1. if it is currentpageIdx is same as index, skip writing
        # and page.data is not full
        # and self.currentPage.id == page.id:
        if self.currentPageIndex == index and page.data[index] != 255:
            return
        # 2. otherwise write
        self.currentPageIndex = index
        self.currentPage = page
        return self.fileManager.writePage(index, page)

    def flush(self):
        # when program shut down, write current page to DB
        return self.fileManager.writePage(self.currentPageIndex, self.currentPage)
