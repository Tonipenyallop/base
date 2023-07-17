from bitmap import Bitmap


class Page:
    def __init__(self, data: bytes, wordLength=5,
                 bitmapLength=1,
                 bitmapSize=8, currentPageIndex=0) -> None:
        self.data = data
        self.wordLength = wordLength
        self.bitmapLength = bitmapLength
        self.bitmapSize = bitmapSize
        self.pageLength = self.wordLength * self.bitmapSize + self.bitmapLength
        self.currentPageIndex = currentPageIndex

    def read(self, index: int) -> list[int] or None:
        # check bitmap the given location is available
        bitmap = Bitmap(self.data[0], bitmapSize=self.bitmapSize)
        if (bitmap.get(index, findFreeSpace=True)):
            return None

        startPoint = (index * self.wordLength) + self.bitmapLength
        return self.data[startPoint: startPoint + self.wordLength]

    def delete(self, index: int) -> None:
        bitmap = Bitmap(self.data[0], bitmapSize=self.bitmapSize)
        bitmap.unset(index)
        self.data[0] = bitmap.data

    def write(self, input: list[str]) -> int:
        bitmap = Bitmap(self.data[0], bitmapSize=self.bitmapSize)
        nextFreeSlot = bitmap.nextFreeIndex()
        if (nextFreeSlot == -1):
            return -1

        startPoint = (nextFreeSlot * self.wordLength) + self.bitmapLength
        self.data[startPoint: startPoint + self.wordLength] = input

        bitmap.set(nextFreeSlot)
        self.data[0] = bitmap.data
        return nextFreeSlot

    def hasFreeSpace(self) -> bool:
        return Bitmap(self.data[0], bitmapSize=self.bitmapSize).nextFreeIndex() != -1

    def getCurrentIndex(self) -> int:
        return self.currentPageIndex
