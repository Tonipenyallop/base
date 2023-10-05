from fileLogger import FileLogger


class MockFileManager:
    def __init__(self, fileLogger: FileLogger) -> None:
        self.readCount: int = 0
        self.writeCount: int = 0
        self.seekCount: int = 0
        self.fileLogger = fileLogger

    def getPage(self) -> int:
        self.readCount += 1
        self.seekCount += 1

    def writePage(self, fakeInput1, fakeInput2) -> int:
        self.writeCount += 1
        self.seekCount += 1
