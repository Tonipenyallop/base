from fileManager import FileManager
from page import Page
from clock import Clock


class PageBuffer:
    def __init__(self, fileManager: FileManager) -> None:
        self.fileManager = fileManager
        self.currentPageIndex: int = 0
        # make it 6
        self.maxSize = 6
        self.currentPinedPages = {}
        self.currentPage: Page = None
        self.isDirty = False
        # self.clock = Clock()

    def getPage(self, pageIndex) -> Page:
        # WHAT IS LEAST USED PAGE
        # use clock policy for that

        # 2. Pin the page and return its address
        if self.currentPageIndex in self.currentPinedPages:
            return self.currentPage
        # 3. check we have extra space or not
        isMaxSize = len(self.currentPinedPages.keys()) == self.maxSize

        # self.currentPageIndex = pageIndex
        # isMaxSize = len(self.currentPinedPages) == self.maxSize
        # print("len(self.currentPinedPages)")
        # print(len(self.currentPinedPages))
        if isMaxSize:
            print('pool is full from get')
            # self.clock.replaceFrame(
            # self.currentPageIndex, self.currentPinedPages[self.currentPageIndex])
            return

        # 3.5 if (isMaxSize) run clock algorithm and replace least used frame
        # 3.5 else just add to currnet pin page
        self.currentPinedPages[pageIndex] = self.fileManager.getPage(pageIndex)
        return self.currentPinedPages[pageIndex]

    def writePage(self, pageIndex: int, page: Page) -> None:
        # 1. if it is currentpageIdx is same as index, skip writing
        if self.currentPageIndex in self.currentPinedPages and page.data[pageIndex] != 255:
            return
        # self.currentPageIndex = pageIndex
        # 2. check we have extra space or not
        isMaxSize = len(self.currentPinedPages.keys()) == self.maxSize
        if isMaxSize:
            print('pool is full from write')
            # self.clock.replaceFrame(
            #     self.currentPageIndex, self.currentPinedPages[self.currentPageIndex])
            return

        # 2.5 if (isMaxSize) run clock algorithm and replace least used frame
        # 2.5 else just add to currnet pin page
        self.currentPinedPages[pageIndex] = self.fileManager.getPage(pageIndex)
        self.currentPage = self.currentPinedPages[pageIndex]
        # 3. otherwise write
        return self.fileManager.writePage(pageIndex, page)

    def flush(self):
        # when program shut down, write current page to DB
        return self.fileManager.writePage(self.currentPageIndex, self.currentPage)
