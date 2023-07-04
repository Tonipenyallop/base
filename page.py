from bitmap import Bitmap


class Page:
    def __init__(self, bitmap=0b0) -> None:
        self.bitmap = Bitmap(bitmap)
        self.data = [bitmap]

    def read(self, index: int) -> list[int] or None:
        # check bitmap the given location is available
        bitmap = Bitmap(self.bitmap)
        if (bitmap.get(index)):
            print('inside get')
            return None

        wordLength = 5
        bitmapLength = 1

        startPoint = (index * wordLength) + bitmapLength
        return self.data[startPoint: startPoint + wordLength]

    def delete(self, index: int) -> None:
        bitmap = Bitmap(self.bitmap)
        bitmap.unset(index)
