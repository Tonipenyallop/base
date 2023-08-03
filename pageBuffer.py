from fileManager import FileManager
from page import Page
from clock import Clock
from node import Node


class PageBuffer:
    def __init__(self, fileManager: FileManager) -> None:
        self.fileManager = fileManager
        self.currentPageIndex: int = 0
        self.currentPage: Page = None
        self.isDirty = False

    def getPage(self, pageIndex) -> Page:
        # if requesting the known page return it
        if pageIndex == self.currentPageIndex:
            return self.currentPage

        # otherwise we don't know this page
        # flush any unsaved data and update our frame of reference
        self.flush()
        self.currentPageIndex = pageIndex
        self.currentPage = self.fileManager.getPage(pageIndex)
        return self.currentPage

    def writePage(self, pageIndex: int, page: Page) -> None:
        # if the page index has change then save what we have currently in memory
        # and start thinking about the new index
        if not self.currentPageIndex == pageIndex:
            self.flush()
            self.currentPageIndex = pageIndex

        # update our knowledge and record that we have unsaved data that needs flushing
        self.currentPage = page
        self.isDirty = True

    def flush(self):
        # when program shut down, write current page to DB
        if self.isDirty and self.currentPage is not None:
            return self.fileManager.writePage(self.currentPageIndex, self.currentPage)
