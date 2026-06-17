from fileManager import FileManager
from page import Page
from clock import Clock
from node import Node
from typing import Dict


class ClockBuffer:
    # A buffer pool holding up to `maxSize` pages in memory, using the CLOCK
    # (second-chance) policy to choose a victim when the pool is full.
    #
    # Single source of truth:
    #   - pinnedPagesQueue: the frames, in clock order (each Node carries its
    #     pageIndex, page, reference bit and dirty bit).
    #   - pagePool: a {pageIndex: page} mirror for O(1) lookup and flush-on-exit.
    # The two are always kept in sync: every frame in the queue has exactly one
    # entry in the pool, and vice versa.
    def __init__(self, fileManager: FileManager, maxSize=6) -> None:
        self.fileManager = fileManager
        self.maxSize = maxSize
        self.pinnedPagesQueue: list[Node] = []
        self.pagePool: Dict[int, Page] = {}
        self.clock = Clock(maxSize)

        # kept only for backward compatibility with callers that read them
        self.currentPageIndex: int = 0
        self.currentPage: Page = None

    def _frameOf(self, pageIndex: int) -> Node or None:
        for node in self.pinnedPagesQueue:
            if node.pageIndex == pageIndex:
                return node
        return None

    def getPage(self, pageIndex: int) -> Page or None:
        # cache hit
        if pageIndex in self.pagePool:
            node = self._frameOf(pageIndex)
            if node is not None:
                node.referenceBit = True
            return self.pagePool[pageIndex]

        # cache miss: load from disk and admit into the pool
        page = self.fileManager.getPage(pageIndex)
        if page is None:
            return None
        self._admit(pageIndex, page, isDirty=False)
        return page

    def writePage(self, pageIndex: int, page: Page) -> None:
        node = self._frameOf(pageIndex)
        if node is not None:
            # update an already-cached frame in place
            node.page = page
            node.referenceBit = True
            node.isDirty = True
            self.pagePool[pageIndex] = page
        else:
            self._admit(pageIndex, page, isDirty=True)

    def _admit(self, pageIndex: int, page: Page, isDirty: bool) -> None:
        if len(self.pinnedPagesQueue) >= self.maxSize:
            self._evict()

        node = Node(pageIndex, page)
        node.referenceBit = True
        node.isDirty = isDirty
        self.pinnedPagesQueue.append(node)
        self.pagePool[pageIndex] = page

        self.currentPageIndex = pageIndex
        self.currentPage = page

    def _evict(self) -> None:
        victimPos = self.clock.findVictim(self.pinnedPagesQueue)
        victim = self.pinnedPagesQueue.pop(victimPos)
        del self.pagePool[victim.pageIndex]
        if victim.isDirty:
            self.flush(victim.pageIndex, victim.page)

    def flush(self, pageIndex: int, page: Page):
        # write a page back to disk
        if page is not None:
            return self.fileManager.writePage(pageIndex, page)
