from fileManager import FileManager
from page import Page
from pageBuffer import PageBuffer
import signal
import sys
import os.path
print('DB initialized')
wordLength = 5
bitmapLength = 1
bitmapSize = 8

pageLength = wordLength * bitmapSize + bitmapLength


def getUnfilledIndexAndPage(fileManager: FileManager) -> tuple[int, Page]:
    unfilledPageIndex = 0
    unfilledPage = None

    totalPagesNumber = file.seek(0, os.SEEK_END) // pageLength

    for _ in range(totalPagesNumber + 1):
        # read the page from the file for the current index
        unfilledPage = fileManager.getPage(unfilledPageIndex)

        # check to see if the page is full
        if (unfilledPage.hasFreeSpace()):
            return [unfilledPageIndex, unfilledPage]
        else:
            unfilledPageIndex += 1


file = open('data/data-0.bin', 'rb+')
fileManager = FileManager(file)
pageBuffer = PageBuffer(fileManager)
# pageBuffer = fileManager

# wordLength = 5
# bitmapLength = 1
# bitmapSize = 8

# pageLength = wordLength * bitmapSize + bitmapLength

unfilledPageIndex, unfilledPage = getUnfilledIndexAndPage(fileManager)


def seeYa(signum, frame):
    pageBuffer.flush()
    print('see ya')
    sys.exit(0)


signal.signal(signal.SIGINT, seeYa)
# header 1byte
# each record = 5 length
# number of records = 8
# how many of bytes => 41

while True:
    try:
        inputValue = input()
    except EOFError:
        break

    if inputValue == 'fini':
        break

    if inputValue[:4] == 'read':
        pageIndex = int(inputValue[5])
        rowIndex = int(inputValue[7])

        if rowIndex not in range(8):
            print('input range must be from 0 to 7')
            continue

        page = pageBuffer.getPage(pageIndex)
        record = page.read(rowIndex)

        if not record:
            print('record not found')
        else:
            print(record.decode())

    if inputValue[:6] == 'delete':
        pageIndex = int(inputValue[7])
        rowIndex = int(inputValue[9])
        # 1. get the page
        unfilledPage = fileManager.getPage(pageIndex)
        # 1.5 update unfilledPageIndex
        unfilledPageIndex, _ = getUnfilledIndexAndPage(fileManager)
        # 2. delete item at index
        unfilledPage.delete(rowIndex)

        # for DB
        # 1. calculate the unfilledPage index of file
        startPageIndex = pageLength * pageIndex
        # 2. move pointer
        file.seek(startPageIndex)
        #  3. overwrite bitmap in unfilledPage
        file.write(unfilledPage.data)
        print(f"{pageIndex}:{rowIndex} was deleted successfully")

    if inputValue[:5] == 'write':
        writeValue = inputValue[6:]
        inputAsBytes = bytearray(writeValue, encoding='utf-8')

        # for local memory
        # 1. check bitmap is full or not. if it's full,
        record = unfilledPage.write(inputAsBytes)
        if record == -1:
            data = bytearray(pageLength)
            # 1.a. create new page
            unfilledPage = Page(data, wordLength, bitmapLength, bitmapSize)
            # 1.b. insert new data to local memory
            record = unfilledPage.write(inputAsBytes)
            # 1.c update index as new page is created
            unfilledPageIndex += 1
        # 2. after adding data and page is full,

        if not unfilledPage.hasFreeSpace():
            # 2.a flush
            pageBuffer.currentPageIndex = unfilledPageIndex
            pageBuffer.currentPage = unfilledPage
            pageBuffer.flush()
            # pageBuffer.writePage(unfilledPageIndex,
            #                      unfilledPage)
            # 2.b update page index and page
            unfilledPageIndex, unfilledPage = getUnfilledIndexAndPage(
                fileManager)

        print(f'{unfilledPageIndex}:{record}-{writeValue}')
        # for DB
        # 3. update DB
        pageBuffer.writePage(unfilledPageIndex, unfilledPage)

# before exiting code, add to db
pageBuffer.flush()
