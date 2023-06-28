import uuid
import os
print('DB initialized')

# localMemory = []
if len(os.listdir('data/')) == 0:
    open('data/data-0.txt', 'x')
sortedDir = [os.path.join('data/', f) for f in os.listdir('data/')
             if os.path.isfile(os.path.join('data/', f))]


# for dir in sortedDir:
#     with open(dir) as file:
#         localMemory.extend(file.read().replace('\n', ',').split(','))
# print(localMemory)
# latestDataLength = len(localMemory)
headerLength = 3
recordLength = 5
latestFile = open(sortedDir[0], 'r+')
while True:
    try:
        inputValue = input()
    except EOFError:
        break

    if inputValue == 'fini':
        break

    if inputValue[:4].lower() == 'read':
        print("inputValue[4]")
        print(inputValue[4])
        pageIndex = int(inputValue[5]) - 1
        index = int(inputValue[6:]) - 1
        reversedSortedDirForRead = sortedDir[::-1]
        currentFile = open(reversedSortedDirForRead[pageIndex], 'r+')
        currentFile.seek(headerLength + recordLength * index)
        print(currentFile.read(recordLength))

    if inputValue[:6].lower() == 'delete':

        print('delete was called')
        reversedSortedDirForDelete = sortedDir[:: -1]
        pageIndex = int(inputValue[7]) - 1  # for index
        index = int(inputValue[8:]) - 1

        if index not in range(8):
            print('index should be between 1 to 8')
            break

        with open(reversedSortedDirForDelete[pageIndex], 'r+') as file:
            bitmap = int(file.read()[0:headerLength].strip())

        bitmapToBinary = format(bitmap, '08b')[::-1]
        deletedBinary = bitmapToBinary[:index] + \
            '0' + bitmapToBinary[index + 1:]

        indexForDelete = index * recordLength + headerLength
        with open(reversedSortedDirForDelete[pageIndex], 'r+') as file:
            file.seek(indexForDelete)
            # delete means make empty space
            file.write('     ')
            file.seek(0)
            decodedBitmap = str(
                int(deletedBinary[::-1], 2)).zfill(headerLength)
            file.write(decodedBitmap)
            print('delete completed')

    if inputValue[:6].lower().strip() == 'write':
        pageIndex = None

        bitmap = None

        for idx, directory in enumerate(sortedDir[::-1]):
            with open(directory, 'r+') as file:
                if (file.read()[0:headerLength] == ''):
                    file.write('000')

                file.seek(0)
                bitmap = int(file.read()[0:headerLength].strip())

                if bitmap < 255:
                    pageIndex = idx
                    break
                elif idx == len(sortedDir) - 1 and bitmap == 255:
                    # Because adding new page, adding index + 1
                    pageIndex = idx + 1
                    print(f'all of dir is full : {idx}, bitmap : {bitmap}')
                    # 1. add default index which is 0
                    with open(f'data/data-{uuid.uuid4()}.txt', 'x+') as file:
                        if (file.read()[0:headerLength] == ''):
                            file.write('000')
                        file.seek(0)

                    # 2. reset bitmap
                    bitmap = 0
                    # 3. update directory we are using
                    sortedDir = [os.path.join('data/', f) for f in os.listdir('data/')
                                 if os.path.isfile(os.path.join('data/', f))]

        bitmapToBinary = format(bitmap, '08b')[::-1]
        reversedSortedDirForWrite = sortedDir[::-1]

        for idx, i in enumerate(bitmapToBinary):

            if i == '0':
                # write logic
                with open(reversedSortedDirForWrite[pageIndex], 'r+') as file:
                    addingIndex = (idx) * recordLength + headerLength
                    # 3 is the maximum length of memory index
                    file.seek(addingIndex)
                    file.write(inputValue[6:])
                    # update bitmap logic
                    file.seek(0)
                    # update current index of bitmap to be 1
                    bitmapToBinary = bitmapToBinary[:idx] + \
                        '1' + bitmapToBinary[idx + 1:]
                    # getting index of bitmap -> reverse updatedBitmapIndex and convert it to integer
                    updatedBitmapIndex = int(bitmapToBinary[::-1], 2)
                    # fill out bitmap index with 0 if updatedBitmapIndex is one or two digit(s)
                    file.write(str(updatedBitmapIndex).zfill(headerLength))
                    print(
                        f"pageIndex : {pageIndex}, addingIndex : {addingIndex}")
                    break

    else:
        raise RuntimeError('input shold be read, write or delete')
