class Bitmap:
    def __init__(self, data=0b0, bitmapSize=8) -> None:
        self.data = data
        self.bitmapSize = bitmapSize

    def get(self, index: int, findFreeSpace: bool = False) -> bool:
        if not findFreeSpace:
            return (self.data >> index) & 1 == 1
        else:
            return (self.data >> index) & 1 == 0

    def set(self, index: int) -> None:
        assert index < self.bitmapSize

        self.data |= 1 << index

    def unset(self, index: int) -> None:
        # why this is working?(homework)
        # -> 1. ig)          10101
        # -> 2. n = 2        00100
        # -> 3. ~00100  =    11011
        # -> 4. use '&'
        #  for 1 and 3  ->   10101
        #                  & 11011
        #                    10001 which is unseted ver of #1
        self.data &= ~(1 << index)

    def nextFreeIndex(self) -> int:
        for index in range(self.bitmapSize):
            if self.get(index, findFreeSpace=True):
                return index
        return -1
