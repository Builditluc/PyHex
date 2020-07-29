# PyHex
# Made by Builditluc

import curses
from base import Application, Window


class HexFile(object):
    def __init__(self, filename:str, columns:int):
        super(__class__, self).__init__()
        self.columns = columns

        self.filename = filename
        self.file_content = bytes

        self.hex_array = []

    def start(self):
        self._readFile()
        self._processContent()
        self._formatContent()

    def _readFile(self):
        # Read the File in binary mode
        self.file_content = open(self.filename, "rb").readlines()

    def _processContent(self):
        # Convert the File Content into Hex

        # Go through every line and convert every byte into Hex
        for line in self.file_content:
            for byte in line:
                hex_byte = hex(byte).replace("x", "").upper()
                if byte >= 16:
                    hex_byte = hex_byte.lstrip("0")
                self.hex_array.append(hex_byte)

    def _formatContent(self):
        # Formats the Hex Array

        i = 0
        line = []
        new_array = []
        for byte in self.hex_array:
            if i == self.columns:
                new_array.append(line)
                line = []
                i = 0

            line.append(byte)
            i += 1

        if line != []:
            new_array.append(line)

        self.hex_array = new_array

class PyHex(Window):
    def __init__(self, *args, **kwargs):
        super(__class__, self).__init__(*args, **kwargs)
        self.initColors()

        # Hiding the Cursor
        self.setCursorState(0)

        self.correctSize = True

        # Creating the variables for the title
        self.title = "PyHex - A Python Hex Editor"

        self.title_x = int
        self.title_y = 0

        # Creating the variables for the Offset text
        self.offset_title = "Offset (h)"
        self.offset_title_x = 1
        self.offset_title_y = 1

        self.offset_len = 8

        # Creating the variables for the Encoded text
        self.encoded_title = ""
        self.encoded_title_x = 13
        self.encoded_title_y = 1

        self.encoded_title_len = 16

        # Creating the variables for the Decoded text
        self.decoded_title = "Decoded text"
        self.decoded_title_x = int
        self.decoded_title_y = 1

        # The File
        self.filename = "test_file.txt"
        self.file = HexFile(self.filename, self.encoded_title_len)
        self.file.start()

    def initColors(self):
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Plaintext color
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)  # Title color

    def update(self):
        # Calculating the coordinates of the title
        self.title_x = int((self.width // 2) - (len(self.title) // 2) - len(self.title) % 2)

        # Generating the Encoded title
        self.encoded_title = ""
        for i in range(0, self.encoded_title_len):
            hex_ch = hex(i).replace("x", "").upper()
            if i >= 16:
                hex_ch = hex_ch.lstrip("0")
            self.encoded_title += hex_ch + " "

        # Calculating the coordinates of the Decoded title
        self.decoded_title_x = self.encoded_title_x + len(self.encoded_title) + 2

        # Calculating the offset
        total_lines = len(self.file.hex_array)
        self.offset_content = []
        for i in range(0, total_lines):
            offset = hex(i * self.encoded_title_len).replace("x", "").upper()
            offset = "0"*(self.offset_len-len(str(offset))) + str(offset)
            self.offset_content.append(offset)

    def lateUpdate(self):
        # Drawing the title
        self.drawText(self.title_y, self.title_x,
                      self.title, 2)

        # Drawing the Offset text
        self.drawText(self.offset_title_y, self.offset_title_x,
                      self.offset_title, 1)

        # Drawing the Encoded text
        self.drawText(self.encoded_title_y, self.encoded_title_x,
                      self.encoded_title, 1)

        # Drawing the Decodeded title
        self.drawText(self.decoded_title_y, self.decoded_title_x,
                      self.decoded_title, 1)

        # Drawing the Content of the File
        y = self.encoded_title_y + 1
        x = self.encoded_title_x
        x_offset = 0
        for line in self.file.hex_array:
            for byte in line:
                self.drawText(y, x + x_offset, byte, 1)
                x_offset += 3
            x_offset = 0
            y += 1

        # Drawing the Offset
        y = self.offset_title_y + 1
        x = self.offset_title_x
        for offset in self.offset_content:
            self.drawText(y, x, offset, 1)
            y += 1

if __name__ == '__main__':
    app: Application = Application()
    app.setMainWindow(PyHex(app.stdscr, app))
    app.run()
