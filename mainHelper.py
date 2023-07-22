from page import Page
from fileManager import FileManager


class MainHelper:
    def __init__(self) -> None:
        pass

    def getUnfilledIndexAndPage(self) -> tuple[int, Page]:
        unfilledPageIndex = 0
        unfilledPage = None
        # while we haven't found the page that we're looking for
        while True:
            # read the page from the file for the current index
            unfilledPage = self.getPage(unfilledPageIndex)

            # check to see if the page is full
            if (unfilledPage.hasFreeSpace()):
                return [unfilledPageIndex, unfilledPage]
            else:
                unfilledPageIndex += 1
