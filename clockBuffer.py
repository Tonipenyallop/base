from fileManager import FileManager
from page import Page
from clock import Clock
from node import Node
from typing import Dict


# logic
#  able to store at most 6 pages

# write
# 1.when replace page, flush
# 2.if current page is different from input page and current page is dirty -> flush

# get
# 1.if it needs to replace page -> flush
# 2.if current page is different from input page and current page is dirty -> flush

# condition :replace
# 1. check page is in pool
# 2. if so, just return
# 3, if pool is full and input page is not in pool -> replace it

# logic :replace
# 1. create a queue
# 2. if reference bit is unset, replace it
# 3. else unset reference bit and move pointer to next unit

# props
# 1. pointer
# 2. queue : list['node'] referenceBit, pageIndex, page, isDirty
# 3. pool


class ClockBuffer:
    def __init__(self, fileManager: FileManager, maxSize=6) -> None:
        self.fileManager = fileManager
        self.maxSize = maxSize
        self.currentPageIndex: int = 0
        self.currentPage: Page = None

        # for clock algorithm
        self.pinnedPagesQueue: list[Node] = [
            None, None, None, None, None, None]

        # for storing page with pageIndex locally
        self.pagePool: Dict[int, Page] = {}
        self.pointer = None
        self.clock = Clock(maxSize)

    def getPage(self, pageIndex) -> Page:
        # WHAT IS LEAST USED PAGE
        # use clock policy for that

        # if requesting the known page return it
        if pageIndex in self.pagePool:
            return self.pagePool[pageIndex]

        # otherwise I do not know this page -> update pool
        if (len(self.pagePool.keys()) < 6):
            self.pagePool[pageIndex] = self.fileManager.getPage(pageIndex)

        # if pool is not full, update page pool
        # otherwise, replace it
        if len(self.pinnedPagesQueue) == self.maxSize:

            [replacedFrame, replacedNode] = self.clock.replaceFrame(
                self.currentPageIndex, self.currentPage, self.pinnedPagesQueue)
            # self.currentPageIndex, self.pagePool[self.currentPageIndex-1], self.pinnedPagesQueue)
            return

        if self.currentPageIndex == pageIndex:
            return self.currentPage

        self.pinnedPagesQueue[self.currentPageIndex].isDirty
        self.currentPageIndex = pageIndex
        self.currentPage = self.fileManager.getPage(pageIndex)
        self.pinnedPagesQueue.append(
            Node(pageIndex, self.currentPage))

    def writePage(self, pageIndex: int, page: Page) -> None:
        # 1. if stored page needs to be replaced, flush.
        # 2. else store to local pagePool

        # what happen if current page is different from input page?

        # 2.if not stored in local page, and pagepool is full, replace it and flush
        if pageIndex not in self.pagePool and len(self.pagePool.keys()) == self.maxSize:
            # if pageIndex not in self.pagePool and len(self.pagePool.keys()) == self.maxSize:
            [replacedFrameIndex, replacedNode] = self.clock.replaceFrame(
                pageIndex, page, self.pinnedPagesQueue)

            #  if page was not replaced,return
            if (replacedFrameIndex == -1 or replacedNode == -1):
                return

            # for storing replaced frame to DB
            self.flush(replacedFrameIndex, replacedNode)

        # 2.otherwise, there is or not, update local page
        else:
            self.pagePool[pageIndex] = page
        # # 4. update current page index
        self.currentPage = page
        self.currentPageIndex = pageIndex

    def flush(self, pageIndex: int, page: Page):
        # when program shut down, write current page to DB
        if self.currentPage is not None:
            return self.fileManager.writePage(pageIndex, page)
