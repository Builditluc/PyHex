from typing import List
import os

class HexFile:
    def __init__(self, path: str) -> None:
        if type(path) != str: raise ValueError
        file_content = self._readFile(path)
        self.converter = HexConverter(file_content)
    
    def _readFile(self, path: str) -> bytes:
        if not os.path.exists(path): raise FileNotFoundError
        with open(path, "rb") as f:
            return f.read()

    @property
    def hex(self) -> List[str]: return self.converter.hex()
    @property
    def ascii(self) -> List[str]: return self.converter.ascii()

class HexConverter:
    def __init__(self, content: bytes) -> None:
        if type(content) != bytes: raise ValueError
        self.bytes = content
    
    def hex(self) -> List[str]:
        hex_data = [hex(byte) for byte in self.bytes]
        hex_data = [hex_val.replace("x", "").lstrip("0").upper() for hex_val in hex_data]
        for (i, hex_val) in enumerate(hex_data):
            if hex_val == "": hex_data[i] = "00"
        return hex_data

    def ascii(self) -> List[str]:
        ascii_data: List[str] = []
        for hex in self.hex():
            try: 
                ascii_char = bytes.fromhex(hex).decode("ascii")
                if ascii_char in [" ", "\x00"]: raise ValueError
                else: ascii_data.append(ascii_char)
            except ValueError: ascii_data.append(".")
        return ascii_data
