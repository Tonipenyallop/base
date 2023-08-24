from page import Page
from node import Node


class Clock:
    def __init__(self) -> None:
        self.clockHand: int = 0
        self.maxSize = 6
        self.referenceBit = True

    # 1. if size of frame pool is not full, return because doesn't need to replace it
    # 2. if framepool contains -> return to node.pageIndex
    # 3. otherwise, run clock policy
    def replaceFrame(self, pageIndex: int, page: Page, framePool: list[Node]) -> tuple[int, Node]:
        # check framePool is full or not
        # check all framePool nodes are None for error handling
        isAllFramePoolNone = True
        insertNodeTo = 0
        for i, node in enumerate(framePool):
            if node:
                isAllFramePoolNone = False
                insertNodeTo = i
                break

        if isAllFramePoolNone or len(framePool) < self.maxSize:
            # updateFramePool
            framePool[insertNodeTo] = Node(pageIndex, page)

            return -1
        # it means framePool already contains current node
        for node in framePool:
            if node and pageIndex == node.pageIndex:
                # update reference bit to True
                node.referenceBit = True
                return -1

        while True:
            if (framePool[self.clockHand].referenceBit):
                framePool[self.clockHand].referenceBit = False
                if self.clockHand == self.maxSize - 1:
                    self.clockHand = 0
                else:
                    self.clockHand += 1
            else:
                # 1. replace current position of node to be incoming node
                node = Node(pageIndex, page)
                previousNode = framePool[self.clockHand]
                framePool[self.clockHand] = node

                # 2. updating clock hand one unit forward
                # 2.a. framePool size is max(6) size
                if (self.clockHand == self.maxSize):
                    self.clockHand = 0
                    print(self.clockHand)
                    return [self.maxSize, previousNode]
                else:
                    self.clockHand += 1
                    print(self.clockHand)
                    return [self.clockHand - 1, previousNode]
