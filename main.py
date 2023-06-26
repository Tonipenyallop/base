import uuid
import os
print('DB initialized')

# localMemory = []

sortedDir = [os.path.join('data/', f) for f in os.listdir('data/')
             if os.path.isfile(os.path.join('data/', f))]


# for dir in sortedDir:
#     with open(dir) as file:
#         localMemory.extend(file.read().replace('\n', ',').split(','))
# print(localMemory)
# latestDataLength = len(localMemory)
headerLength = 1
recordLength = 5
latestFile = open(sortedDir[0], 'r+')
while True:

    inputValue = input()
    if inputValue == 'fini':
        break

    if inputValue[:4].lower() == 'read':
        index = int(inputValue[4:])
        currentFile = open(sortedDir[0], 'r+')
        currentFile.seek(headerLength + recordLength * index)
        print(currentFile.read(recordLength))

    if inputValue[:6].lower() == 'delete':
        print('delete was called')
        index = int(inputValue[6:]) - 1

        if index not in range(8):
            print('index should be between 1 to 8')
            break
        with open(sortedDir[0], 'r+') as file:
            bitmap = int(file.read()[0:3].strip())

        bitmapToBinary = format(bitmap, '08b')[::-1]
        deletedBinary = bitmapToBinary[:index] + \
            '0' + bitmapToBinary[index + 1:]

        indexForDelete = index * recordLength + 3
        with open(sortedDir[0], 'r+') as file:
            file.seek(indexForDelete)
            # delete means make empty space
            file.write('     ')
            file.seek(0)
            decodedBitmap = str(int(deletedBinary[::-1], 2))
            file.write(decodedBitmap)
            print('delete completed')

    if inputValue[:6].lower().strip() == 'write':
        pageNumber = 1
        # todo
        # 1. if no empty space, reject
        # 2. else add to empty space
        # 3. update bitmap
        # print row number
        bitmap = None
        with open(sortedDir[0], 'r+') as file:
            # bitmap is in range of 0 - 255
            bitmap = int(file.read()[0:3].strip())
            if bitmap == 255:
                print('No space available')
                break

        bitmapToBinary = format(bitmap, '08b')[::-1]

        for idx, i in enumerate(bitmapToBinary):

            if i == '0':
                # write logic
                with open(sortedDir[0], 'r+') as file:
                    addingIndex = (idx) * recordLength + 3
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
                    file.write(str(updatedBitmapIndex).zfill(3))
                    print(
                        f"pageNumber : {pageNumber}, addingIndex : {addingIndex}")
                    break

# 0. update: read and delete(page, line)
# 1. write -> position of put it(print page number(default 1) and index)
