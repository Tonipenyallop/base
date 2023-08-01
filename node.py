from page import Page


class Node:
    def __init__(self, pageIndex: int, page: Page) -> None:
        self.referenceBit = True
        self.pageIndex = pageIndex
        self.page = page
