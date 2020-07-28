# PyHex
# Made by Builditluc

import curses
from base import Application, Window


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

        # Creating the variables for the Encoded text
        self.encoded_title = ""
        self.encoded_title_x = 13
        self.encoded_title_y = 1

        self.encoded_title_len = 25

        # Creating the variables for the Decoded text
        self.decoded_title = "Decoded text"
        self.decoded_title_x = int
        self.decoded_title_y = 1

        # The Path of the opened File
        self.file_path = "test_file.txt"

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


if __name__ == '__main__':
    app: Application = Application()
    app.setMainWindow(PyHex(app.stdscr, app))
    app.run()
