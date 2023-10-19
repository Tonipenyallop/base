class MockFile:
    def __init__(self, returnValue: int) -> None:
        self.returnValue = returnValue

    def seek(self, _zero, _seekEnd):
        return self.returnValue
