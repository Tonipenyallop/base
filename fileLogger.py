from io import FileIO


class FileLogger:
    def __init__(self, file: FileIO) -> None:
        # 1. recieve file
        self.file = file
        self.readCount = 0
        self.seekCount = 0
        self.writeCount = 0

    # 2. implements all of the file methods we use
    def read(self, startIndex: int):
        self.readCount += 1
        return self.file.read(startIndex)

    def write(self, data: bytes):
        self.writeCount += 1
        return self.file.write(data)

    def seek(self, startPageIndex):
        self.seekCount += 1
        return self.file.seek(startPageIndex)

    def close(self):
        result = f"self.readCount:{self.readCount}, self.seekCount:{self.seekCount}, self.writeCount:{self.writeCount}"
        print(result)
        return result

    # 3. read, seek, write, close(for counting other 3 methods)
    # 4. provide a way to get the current count of how many times file are accessed
