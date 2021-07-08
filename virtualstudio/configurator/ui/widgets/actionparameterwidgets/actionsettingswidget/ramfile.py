class RamFile:

    def __init__(self, data: bytes):
        """
        Constructor

        :param data:
        """
        self.ptr: int = 0
        self.data: bytes = data

    def read(self, length: int) -> bytes:
        chunk = self.data[self.ptr: min(len(self.data), self.ptr + length)]
        self.ptr = self.ptr + min(len(self.data), self.ptr + length)
        return chunk

    def reset(self):
        self.ptr = 0