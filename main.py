import uuid
import os


def getLatestDirectory():
    res = ''
    for dir in os.listdir('data/'):
        if res == '':
            res = dir
        else:
            res = max(os.path.getctime('dir'), os.path.getctime(res))
    return res


def getLatestFile(latestDir: str) -> str:
    return open(f'data/{latestDir}', 'r+')


latestDirectory = getLatestDirectory()
maxCounter = 10


def parseData(file: str) -> list[str]:
    return file.read().replace('\n', ',').split(',')


def getAllData(dataDirectory: list[str]) -> list[str]:
    res = []
    for fileElement in dataDirectory:
        file = open(f'{fileElement}', 'r+')
        parsedData = parseData(file)
        for element in parsedData:
            res.append(element)
    return res


def get_files_sorted_by_time(directory):
    # get all files from the given directory
    files = [os.path.join(directory, f) for f in os.listdir(
        directory) if os.path.isfile(os.path.join(directory, f))]

    # sort the files by their creation time
    sorted_files = sorted(files, key=os.path.getctime)

    return sorted_files


# localMemory = getAllData(get_files_sorted_by_time('data/'))

# latestFile = getLatestFile(latestDirectory)
# # latestData = parseData(open(f'data/{latestDirectory}', 'r+'))


# latestDataLength = len(localMemory)

# while True:
#     inputValue = input()
#     if inputValue == 'fini':
#         break

#     # if the current local length reaches max lenght, create a new file and start to write to that file
#     if latestDataLength > maxCounter:
#         latestFile.close()
#         latestFile = open(
#             'data/data-' + str(uuid.uuid4()) + '.txt', 'x+')
#         print('latestFile.read()')
#         print(latestFile.read())
#         # update local memory
#         localMemory = getAllData(os.listdir('data/'))

#     # write to current file
#     latestFile.read()
#     latestFile.write(inputValue + '\n')
#     # update local memory
#     localMemory.append(inputValue)
#     print(*localMemory)
#     # need to update current file size
#     latestDataLength = len(localMemory) // len(os.listdir('data/'))

# create 40 items
for i in range(40):
    # inputValue = input()
    inputValue = str(i)
    print("latestFile")
    print(latestFile)
    # if the current local length reaches max lenght, create a new file and start to write to that file
    if latestDataLength > maxCounter:
        latestFile.close()
        latestFile = open(
            'data/data-' + str(uuid.uuid4()) + '.txt', 'x+')
        # print('latestFile.read()')
        # print(latestFile.read())
        # update local memory
        localMemory = getAllData(get_files_sorted_by_time('data/'))
        # localMemory = getAllData(os.listdir('data/'))

    # write to current file
    latestFile.read()
    latestFile.write(inputValue + '\n')
    # update local memory
    localMemory.append(inputValue)
    print(*localMemory)
    # need to update current file size
    latestDataLength = len(localMemory) // len(os.listdir('data/'))


def getPage(pageNumber: int) -> str:
    return get_files_sorted_by_time('data/')[pageNumber]


def getLine(page: str, lineNumber: int) -> str:
    content = open(page, 'r').read()
    # since last line also contains \n, drop off only last element
    return content.split('\n')[:-1][lineNumber - 1]


getLine(getPage(3), 5)
# getLine(getPage(9), 10)
