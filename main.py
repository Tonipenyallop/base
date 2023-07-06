from page import Page
print('DB initialized')

headerLength = 3
recordLength = 5
file = open('data/data-0.bin', 'rb+')

readFile = bytearray(file.read(41))
if len(readFile) < 41:
    numberOfZero = 41 - len(readFile)
    readFile.extend([0]*numberOfZero)

print(f"database:{readFile}")

page = Page(readFile)
# header 1byte
# each record = 5 length
# number of records = 8
# how many of bytes => 41
while True:

    inputValue = input()

    if inputValue == 'fini':
        break

    if inputValue[:4] == 'read':
        index = int(inputValue[5])
        if index not in range(8):
            print('input range must be from 0 to 7')
            continue
        print(page.read(index))

    if inputValue[:6] == 'delete':
        index = int(inputValue[7])
        # for local memory
        page.delete(index)

        # for DB
        file.seek(0)
        file.write(page.data)
        print(f"index {index} was deleted successfully")

    if inputValue[:5] == 'write':
        writeValue = inputValue[6:]
        inputAsBytes = bytearray(writeValue, encoding='utf-8')
        # for local memory
        if page.write(inputAsBytes) == -1:
            print('no space available')
            break

        # for DB
        file.seek(0)
        file.write(page.data)
        print("page.data")
        print(page.data)
