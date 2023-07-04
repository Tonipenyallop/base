import unittest
from bitmap import Bitmap


class TestBitmap(unittest.TestCase):
    def testGet(self):
        newBitmap = Bitmap()
        newBitmap.data = 0b01100100
        self.assertEqual(False, newBitmap.get(0))
        self.assertEqual(False, newBitmap.get(1))
        self.assertEqual(True, newBitmap.get(2))
        self.assertEqual(False, newBitmap.get(3))
        self.assertEqual(False, newBitmap.get(4))
        self.assertEqual(True, newBitmap.get(5))
        self.assertEqual(True, newBitmap.get(6))
        self.assertEqual(False, newBitmap.get(7))

        self.assertEqual(True, newBitmap.get(0, findFreeSpace=True))
        self.assertEqual(True, newBitmap.get(1, findFreeSpace=True))
        self.assertEqual(False, newBitmap.get(2, findFreeSpace=True))
        self.assertEqual(True, newBitmap.get(3, findFreeSpace=True))
        self.assertEqual(True, newBitmap.get(4, findFreeSpace=True))
        self.assertEqual(False, newBitmap.get(5, findFreeSpace=True))
        self.assertEqual(False, newBitmap.get(6, findFreeSpace=True))
        self.assertEqual(True, newBitmap.get(7, findFreeSpace=True))

    def testSet(self):
        newBitmap = Bitmap()
        newBitmap.data = 0b01100100
        self.assertEqual(False, newBitmap.get(0))
        newBitmap.set(0)
        self.assertEqual(True, newBitmap.get(0))

        self.assertEqual(False, newBitmap.get(7))
        newBitmap.set(7)
        self.assertEqual(True, newBitmap.get(7))

    def testUnset(self):
        newBitmap = Bitmap()
        newBitmap.data = 0b01100100
        self.assertEqual(True, newBitmap.get(2))
        newBitmap.unset(2)
        self.assertEqual(False, newBitmap.get(2))

        self.assertEqual(False, newBitmap.get(3))
        newBitmap.unset(3)
        self.assertEqual(False, newBitmap.get(3))

    def testNextFreeIndex(self):
        newBitmap = Bitmap()
        newBitmap.data = 0b01100100
        self.assertEqual(0, newBitmap.nextFreeIndex())
        newBitmap.set(0)
        self.assertEqual(1, newBitmap.nextFreeIndex())
        newBitmap.set(1)
        self.assertEqual(3, newBitmap.nextFreeIndex())


if __name__ == '__main__':
    unittest.main()
