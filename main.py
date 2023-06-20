import uuid
import os


localMemory = []

sortedDir = [os.path.join('data/', f) for f in os.listdir('data/')
             if os.path.isfile(os.path.join('data/', f))]


for dir in sortedDir:
    with open(dir) as file:
        localMemory.extend(file.read().replace('\n', ',').split(','))
print(localMemory)
latestDataLength = len(localMemory)
latestFile = open(sortedDir[0], 'r+')
while True:

    inputValue = input()
    print("inputValue[:5]")
    print(inputValue[:5])
    if inputValue == 'fini':
        break

    if inputValue[:4].lower() == 'read':
        index = int(inputValue[4:])
        content = open(sortedDir[0], 'r+').readlines()

    if inputValue[:6].lower() == 'delete':
        print('delete was called')
        index = int(inputValue[6:])
        with open(sortedDir[0], 'r+') as file:
            content = file.readlines()
            del content[index - 1]
            file.seek(0)
            file.truncate()
            file.writelines(content)
            # need to update localmemory and print it here
            # localMemory.replace('\n', ',').split(',')
            # print(*localMemory)

    if inputValue[:6].lower().strip() == 'write':
        print('wiriehciow')
    # if the current local length reaches max lenght, create a new file and start to write to that file
        if len(localMemory) > 10:
            latestFile.close()
            latestFile = open(
                'data/data-' + str(uuid.uuid4()) + '.txt', 'x+')

        latestFile.write(inputValue[5:].strip() + '\n')

        # update local memory
        localMemory.append(inputValue[5:].strip())
        print(*localMemory)
        # need to update current file size
        latestDataLength = len(localMemory) // len(os.listdir('data/'))
