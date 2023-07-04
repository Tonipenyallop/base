from bitmap import Bitmap


class Page:
    def __init__(self, bitmap=0b0) -> None:
        self.data = []
        self.bitmap = Bitmap(bitmap)

    def read(self, index: int) -> list[int] or None:
        # check bitmap the given location is available
        if (self.bitmap.get(index, findFreeSpace=True)):
            return None

        wordLength = 5
        bitmapLength = 1

        startPoint = (index * wordLength) + bitmapLength
        return self.data[startPoint: startPoint + wordLength]

    def delete(self, index: int) -> None:
        self.bitmap.unset(index)
        self.data[0] = self.bitmap.data
