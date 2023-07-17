from fileManager import FileManager
from page import Page
print('DB initialized')

file = open('data/data-0.bin', 'rb+')
fileManager = FileManager(file)

wordLength = 5
bitmapLength = 1
bitmapSize = 8

pageLength = wordLength * bitmapSize + bitmapLength

unfilledPageIndex, unfilledPage = fileManager.getUnfilledIndexAndPage()

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

        page = fileManager.getPage(pageIndex)
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
        unfilledPageIndex, _ = fileManager.getUnfilledIndexAndPage()
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
        unfilledPageIndex, unfilledPage = fileManager.getUnfilledIndexAndPage()
        writeValue = inputValue[6:]
        inputAsBytes = bytearray(writeValue, encoding='utf-8')
        # for local memory
        record = unfilledPage.write(inputAsBytes)
        if record == -1:
            data = bytearray(pageLength)
            unfilledPage = Page(data, wordLength, bitmapLength, bitmapSize)
            record = unfilledPage.write(inputAsBytes)
            # todo taesu 1. needs to update new page index to be latest
            unfilledPageIndex += 1

        print(f'{unfilledPageIndex}:{record}')

        # for DB
        startPageIndex = unfilledPageIndex * pageLength
        file.seek(startPageIndex)
        file.write(unfilledPage.data)
