#!/bin/env python3.8
# PyHex
# Made by Builditluc

import curses, curses.ascii ,sys
from base import Application, Window


class HexFile(object):
    def __init__(self, filename: str, columns: int):
        super(__class__, self).__init__()
        self.columns = columns

        self.filename = filename
        self.file_content = bytes

        self.hex_array = []
        self.hex_array_len = 0

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
                self.hex_array_len += 1
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

        if line:
            new_array.append(line)

        self.hex_array = new_array


class PyHex(Window):
    def __init__(self, *args, **kwargs):
        super(__class__, self).__init__(*args, **kwargs)
        self.init_colors()

        # Hiding the Cursor
        self.set_cursor_state(0)

        self.max_lines = curses.LINES - 2  # Max number of lines on the screen
        self.current = 0  # The selected line
        self.top_line = 0  # The line at the top of the screen
        self.bottom_line = 0 # The line at the bottom of the screen

        self.UP = -1
        self.DOWN = 1

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
        self.filename = sys.argv[1]
        #self.filename = "base.py"
        self.file = HexFile(self.filename, self.encoded_title_len)
        self.file.start()

        self.bottom_line = len(self.file.hex_array)

    def init_colors(self):
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Plaintext color
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)  # Title color
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Selected color

    def check_keys(self):
        if self.key_pressed == curses.ascii.ESC:
            sys.exit()

        if self.key_pressed == curses.KEY_UP:
            self.scroll(self.UP)
        elif self.key_pressed == curses.KEY_DOWN:
            self.scroll(self.DOWN)

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
            offset = "0" * (self.offset_len - len(str(offset))) + str(offset)
            self.offset_content.append(offset)


    def late_update(self):
        # Drawing the title
        self.draw_text(self.title_y, self.title_x,
                       self.title, 2)

        # Drawing the Offset text
        self.draw_text(self.offset_title_y, self.offset_title_x,
                       self.offset_title, 1)

        # Drawing the Encoded text
        self.draw_text(self.encoded_title_y, self.encoded_title_x,
                       self.encoded_title, 1)

        # Drawing the Decoded title
        self.draw_text(self.decoded_title_y, self.decoded_title_x,
                       self.decoded_title, 1)

        # Drawing the Content of the File
        y = self.encoded_title_y + 1
        x = self.encoded_title_x
        x_offset = 0

        lines = self.file.hex_array[self.top_line:self.top_line + self.max_lines]

        for i, line in enumerate(lines):
            for byte in line:
                if i == self.current:
                    self.draw_text(y, x + x_offset, byte, 3)
                else:
                    self.draw_text(y, x + x_offset, byte, 1)
                x_offset += 3
            x_offset = 0
            y += 1

        # Drawing the Offset
        y = self.offset_title_y + 1
        x = self.offset_title_x

        offsets = self.offset_content[self.top_line:self.max_lines + self.top_line]

        for offset in offsets:
            self.draw_text(y, x, offset, 1)
            y += 1

        # DEBUG
        #self.draw_text(2, self.title_x, "DEBUG:", 2)
        #self.draw_text(3, self.title_x + 4, "self.top_line : " + str(self.top_line), 1)
        #self.draw_text(4, self.title_x + 4, "self.bottom_line : " + str(self.bottom_line), 1)
        #self.draw_text(5, self.title_x + 4, "self.max_lines : " + str(self.max_lines), 1)
        #self.draw_text(6, self.title_x + 4, "self.current : " + str(self.current), 1)

    def scroll(self, direction):
        """
        Scrolling the window when pressing up/down arrow keys
        :param direction: The direction of the Scrolling (Up or Down)
        """
        # next cursor position after scrolling
        next_line = self.current + direction

        # Up direction scroll overflow
        # current cursor position is 0, but top position is greater than 0
        if (direction == self.UP) and (self.top_line > 0 and self.current == 0):
            self.top_line += direction
            return

        # Down direction scroll overflow
        # next cursor position touch the max lines, but absolute position of max lines could not touch the bottom
        if (direction == self.DOWN) and (next_line == self.max_lines) and (self.top_line + self.max_lines < self.bottom_line):
            self.top_line += direction
            return

        # Scroll up
        # current cursor position or top position is greater than 0
        if (direction == self.UP) and (self.top_line > 0 or self.current > 0):
            self.current = next_line
            return

        # Scroll down
        # next cursor position is above max lines, and absolute position of next cursor could not touch the bottom
        if (direction == self.DOWN) and (next_line < self.max_lines) and (self.top_line + next_line < self.bottom_line):
            self.current = next_line
            return


if __name__ == '__main__':
    app: Application = Application()
    app.set_main_window(PyHex(app.stdscr, app))
    app.run(time_wait=0)
