from fileManager import FileManager
from page import Page
from pageBuffer import PageBuffer
from clockBuffer import ClockBuffer
from fileLogger import FileLogger
from typing import Union
from io import FileIO
import signal
import sys
import os.path
print('DB initialized')
wordLength = 5
bitmapLength = 1
bitmapSize = 8

pageLength = wordLength * bitmapSize + bitmapLength

file = open('data/data-0.bin', 'rb+')
fileLogger = FileLogger(file)
fileManager = FileManager(fileLogger)
pageBuffer = PageBuffer(fileManager)
clockBuffer = ClockBuffer(fileManager)

# change this to control our caching policy
# pageAccessor = fileManager
pageAccessor = clockBuffer
# pageAccessor = pageBuffer

# todo taesu :
# rerunning not working


def readPages(file: FileIO, pageLength: int, pageAccessor: Union[ClockBuffer, PageBuffer]) -> tuple[list[int], int]:
    unfilledPageIndexes: list[int] = []
    fileLength = file.seek(0, os.SEEK_END)
    maxPageIndex = fileLength // pageLength if fileLength > 0 else -1
    print(f"maxPageIndex: {maxPageIndex}")
    if (maxPageIndex >= 1):
        for i in range(maxPageIndex):
            print(f'this is {i} time(s)')
            # read the page from the file for the current index
            # check to see if the page is full

            # why do pages not contain 6 of them
            page = pageAccessor.getPage(i)

            if not page:
                return [unfilledPageIndexes, maxPageIndex]

            if (page.hasFreeSpace()):
                unfilledPageIndexes.append(i)

    return [unfilledPageIndexes, maxPageIndex]


def seeYa(signum, frame):
    for pageIndex in clockBuffer.pagePool.keys():
        clockBuffer.flush(pageIndex, clockBuffer.pagePool[pageIndex])
    print('see ya')
    pageBuffer.fileManager.fileLogger.close()
    sys.exit(0)


def main():
    signal.signal(signal.SIGINT, seeYa)

    [unfilledPageIndexes, maxPageIndex] = readPages(
        file, pageLength, pageAccessor)

    # header 1byte
    # each record = 5 length
    # number of records = 8
    # how many of bytes => 41

    while True:
        try:
            inputValue = input()
        except EOFError:
            break

        print("===== " + inputValue)

        if inputValue == 'fini':
            break

        if inputValue[:4] == 'read':
            pageIndex = int(inputValue[5])
            rowIndex = int(inputValue[7])

            if rowIndex not in range(8):
                print('input range must be from 0 to 7')
                continue

            page = pageAccessor.getPage(pageIndex)

            if page == None:
                print('page not found')
                continue

            record = page.read(rowIndex)
            if not record:
                print('record not found')
                continue
            else:
                print(record.decode())

        if inputValue[:6] == 'delete':
            pageIndex = int(inputValue[7])
            rowIndex = int(inputValue[9])

            page = pageAccessor.getPage(pageIndex)
            page.delete(rowIndex)
            pageAccessor.writePage(pageIndex, page)

            # the page has had things deleted so there is now space
            if pageIndex not in unfilledPageIndexes:
                unfilledPageIndexes.append(pageIndex)

        if inputValue[:5] == 'write':
            # what is the logic for finding next unfilled page and index?
            # 1. array
            page = None
            pageIndex = 0
            # Delete logic
            # 2. if deleted current page which is full, add to the array
            # 2.5. if deleted current page which is NOT full, do NOTHING

            # Wrtie logic
            # if current page is full, update unfilled page to be next page
            # 3. after adding to the memory and
            # if len(unfilledPagesArray) > 0:
            writeValue = inputValue[6:]
            inputAsBytes = bytearray(writeValue, encoding='utf-8')
            print(f"unfilledPageIndexes {unfilledPageIndexes}")
            # for local memory

            # what is unfilled page?
            # 1. completely new page if the data no longer contains available free space
            # 2. first element of array if it is NOT empty
            if len(unfilledPageIndexes) == 0:

                data = bytearray(pageLength)
                page = Page(data, wordLength, bitmapLength, bitmapSize)

                maxPageIndex += 1
                pageIndex = maxPageIndex

                unfilledPageIndexes.append(pageIndex)
            else:
                pageIndex = unfilledPageIndexes.pop()
                page = pageAccessor.getPage(pageIndex)
            record = page.write(inputAsBytes)
            if record == -1:
                raise ValueError('unexpected fulled page')

            print(f'{pageIndex}:{record}-{writeValue}')

            # for DB
            # 3. update DB
            pageAccessor.writePage(pageIndex, page)
            if page.hasFreeSpace() and pageIndex not in unfilledPageIndexes:
                unfilledPageIndexes.append(pageIndex)

    # before exiting code, add to db
    seeYa(None, None)


if __name__ == '__main__':
    main()
