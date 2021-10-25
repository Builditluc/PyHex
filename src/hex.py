from typing import List

class HexFile:
    def __init__(self, path: str) -> None:
        file_content = self._readFile(path)
        self.converter = HexConverter(file_content)
    
    def _readFile(self, path: str) -> bytes:
        return b""

    @property
    def hex(self) -> List[str]: return self.converter.hex()
    @property
    def ascii(self) -> List[str]: return self.converter.ascii()

class HexConverter:
    def __init__(self, bytes: bytes) -> None:
        self.bytes = bytes
    
    def hex(self) -> List[str]:
        return []

    def ascii(self) -> List[str]:
        return []
