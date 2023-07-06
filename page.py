from bitmap import Bitmap


wordLength = 5
bitmapLength = 1
bitmapSize = 8
pageLength = wordLength * bitmapSize + bitmapLength


class Page:
    def __init__(self, data: bytes) -> None:
        assert len(data) == pageLength
        self.data = data

    def read(self, index: int) -> list[int] or None:
        # check bitmap the given location is available
        bitmap = Bitmap(self.data[0])
        if (bitmap.get(index, findFreeSpace=True)):
            return None

        startPoint = (index * wordLength) + bitmapLength
        return self.data[startPoint: startPoint + wordLength]

    def delete(self, index: int) -> None:
        bitmap = Bitmap(self.data[0])
        bitmap.unset(index)
        self.data[0] = bitmap.data

    def write(self, input: list[str]) -> int:
        bitmap = Bitmap(self.data[0])
        bitmapLength = 1
        nextFreeSlot = bitmap.nextFreeIndex()
        if (nextFreeSlot == -1):
            return -1

        startPoint = (nextFreeSlot * wordLength) + bitmapLength
        self.data[startPoint: startPoint + wordLength] = input

        bitmap.set(nextFreeSlot)
        self.data[0] = bitmap.data

        return nextFreeSlot
