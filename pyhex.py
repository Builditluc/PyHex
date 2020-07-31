#!/bin/env python3.8
"""
PyHex is a simple python Hex viewer
"""

import curses
import curses.ascii
import sys
from base import Application, Window


class HexFile:
    """
    This is a class for reading a file and convert
    it to hex
    """

    def __init__(self, filename: str, columns: int):
        super(__class__, self).__init__()
        self.columns = columns

        self.filename = filename
        self.file_content = bytes

        self.hex_array = []
        self.hex_array_len = 0

    def start(self):
        """
        This function begins the process of reading a file
        and converting it to hex
        """
        self._read_file()
        self._process_content()
        self._format_content()

    def decode_hex(self):
        """
        This function decodes the hex content of the file to ascii

        :return: The decoded text, already formatted
        """
        decoded_array = []

        for line in self.hex_array:
            line_array = []
            for hex_object in line:
                # Convert the hex byte into a normal byte
                byte_object = bytes.fromhex(hex_object)

                # Convert the byte into ascii
                ascii_object = byte_object.decode("ascii")

                # Replace the char with a dot if it's a special character
                special_characters = ["\a", "\b", "\f", "\n", "\r", "\t", "\v"]
                if ascii_object in special_characters:
                    ascii_object = "."

                # Add the ascii char to the line array
                line_array.append(ascii_object)

            # add the line to the decoded array
            decoded_array.append(line_array)

        return decoded_array

    def _read_file(self):
        self.file_content = open(self.filename, "rb").readlines()

    def _process_content(self):
        # Convert the File Content into Hex

        # Go through every line and convert every byte into Hex
        for line in self.file_content:
            for byte in line:
                self.hex_array_len += 1
                hex_byte = hex(byte).replace("x", "").upper()
                if byte >= 16:
                    hex_byte = hex_byte.lstrip("0")
                self.hex_array.append(hex_byte)

    def _format_content(self):
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
    """
    This is the PyHex Window that is
    displayed when the program starts
    """

    # pylint: disable=too-many-instance-attributes
    # pylint: disable=no-member
    def __init__(self, *args, **kwargs):
        super(__class__, self).__init__(*args, **kwargs)
        self.init_colors()

        # Hiding the Cursor
        self.set_cursor_state(0)
        self.columns = 16

        self.max_lines = curses.LINES - 3  # Max number of lines on the screen
        self.top_line = 0  # The line at the top of the screen
        self.bottom_line = 0  # The line at the bottom of the screen

        self.cursor_y = 0  # The y coord of the cursor
        self.cursor_x = 0  # The x coord of the cursor
        self.cursor_byte = 0  # The position of the cursor in a single byte (0 or 1)

        self.up_scroll = -1
        self.down_scroll = 1

        self.left_scroll = -1
        self.right_scroll = 1

        # Creating the variables for the title
        self.title = "PyHex - A Python Hex Viewer"

        self.title_x = int
        self.title_y = 0

        # Creating the variables for the Offset text
        self.offset_title = "Offset (h)"
        self.offset_title_x = 2
        self.offset_title_y = 1

        self.offset_len = 8

        self.offset_text = []
        self.offset_text_x = 2
        self.offset_text_y = 2

        # Creating the variables for the Encoded text
        self.encoded_title = ""
        self.encoded_title_x = 14
        self.encoded_title_y = 1

        self.encoded_text_x = 14
        self.encoded_text_y = 2

        # Creating the variables for the Decoded text
        self.decoded_title = "Decoded text"
        self.decoded_title_x = int
        self.decoded_title_y = 1

        self.decoded_text = []
        self.decoded_text_x = int
        self.decoded_text_y = 2

        # The File
        self.filename = sys.argv[1]
        # self.filename = "base.py"
        self.file = HexFile(self.filename, self.columns)
        self.file.start()

        # Decode the File into ascii
        self.decoded_text = self.file.decode_hex()

        # Calculate the bottom line
        self.bottom_line = len(self.file.hex_array)

    def init_colors(self):
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Plaintext color
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)  # Title color
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Selected color

    def check_keys(self):
        if self.key_pressed == curses.ascii.ESC or self.key_pressed == ord("q"):
            sys.exit()

        if self.key_pressed == curses.KEY_UP:
            self.scroll_vertically(self.up_scroll)
        elif self.key_pressed == curses.KEY_DOWN:
            self.scroll_vertically(self.down_scroll)

        if self.key_pressed == curses.KEY_LEFT:
            self.scroll_horizontally(self.left_scroll)
        elif self.key_pressed == curses.KEY_RIGHT:
            self.scroll_horizontally(self.right_scroll)

    def update(self):
        # Calculating the coordinates of the title
        self.title_x = int((self.width // 2) - (len(self.title) // 2) - len(self.title) % 2)

        # Generating the Encoded title
        self.encoded_title = ""
        for i in range(0, self.columns):
            hex_ch = hex(i).replace("x", "").upper()
            if i >= 16:
                hex_ch = hex_ch.lstrip("0")
            self.encoded_title += hex_ch + " "

        # Calculating the coordinates of the Decoded title
        self.decoded_title_x = self.encoded_title_x + len(self.encoded_title) + 3
        self.decoded_text_x = self.decoded_title_x

        # Calculating the offset
        total_lines = len(self.file.hex_array)
        self.offset_text = []
        for i in range(0, total_lines):
            offset = hex(i * self.columns).replace("x", "").upper()
            offset = "0" * (self.offset_len - len(str(offset))) + str(offset)
            self.offset_text.append(offset)

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
        y_coord = self.encoded_text_y + 1
        x_coord = self.encoded_text_x
        x_offset = 0

        lines = self.file.hex_array[self.top_line:self.top_line + self.max_lines]

        for _y, line in enumerate(lines):
            for _x, byte in enumerate(line):
                if _y == self.cursor_y and _x == self.cursor_x:
                    if self.cursor_byte == 0:
                        self.draw_text(y_coord, x_coord + x_offset, byte[:1], 3)
                        self.draw_text(y_coord, x_coord + x_offset + 1, byte[1:], 1)
                    else:
                        self.draw_text(y_coord, x_coord + x_offset, byte[:1], 1)
                        self.draw_text(y_coord, x_coord + x_offset + 1, byte[1:], 3)
                else:
                    self.draw_text(y_coord, x_coord + x_offset, byte, 1)
                x_offset += 3
            x_offset = 0
            y_coord += 1

        # Drawing the Offset
        y_coord = self.offset_text_y + 1
        x_coord = self.offset_text_x

        offsets = self.offset_text[self.top_line:self.max_lines + self.top_line]

        for offset in offsets:
            self.draw_text(y_coord, x_coord, offset, 1)
            y_coord += 1

        # Draw the decoded text
        y_coord = self.decoded_text_y + 1
        x_coord = self.decoded_text_x
        x_offset = 0

        lines = self.decoded_text[self.top_line:self.top_line + self.max_lines]

        for line in lines:
            for char in line:
                self.draw_text(y_coord, x_coord + x_offset, char, 1)
                x_offset += 1
            x_offset = 0
            y_coord += 1

        # DEBUG
        # self.draw_text(2, self.title_x, "DEBUG:", 2)
        # self.draw_text(3, self.title_x + 4, "self.top_line : " + str(self.top_line), 1)
        # self.draw_text(4, self.title_x + 4, "self.bottom_line : " + str(self.bottom_line), 1)
        # self.draw_text(5, self.title_x + 4, "self.max_lines : " + str(self.max_lines), 1)
        # self.draw_text(6, self.title_x + 4, "self.current : " + str(self.current), 1)

    def scroll_horizontally(self, direction):
        """
        Moves the cursor to the left/right using the left/right arrow keys
        :param direction: The direction of the Scrolling (Left or Right)
        """
        # next cursor position after scrolling
        next_position = self.cursor_x + direction

        # Scroll left
        # current cursor position or left position is greater than 0
        if (direction == self.left_scroll) and (self.cursor_x >= 0):
            if self.cursor_byte == 1:
                self.cursor_byte = 0
            else:
                if next_position < 0:
                    return
                self.cursor_x = next_position
                self.cursor_byte = 1
            return

        # Scroll right
        # absolute position of next cursor is not the right edge
        if (direction == self.right_scroll) and (next_position < self.columns + 1):
            if self.cursor_byte == 0:
                self.cursor_byte = 1
            else:
                if next_position >= self.columns:
                    return
                self.cursor_x = next_position
                self.cursor_byte = 0
            return

    def scroll_vertically(self, direction):
        """
        Scrolling the window when pressing up/down arrow keys
        :param direction: The direction of the Scrolling (Up or Down)
        """
        # next cursor position after scrolling
        next_line = self.cursor_y + direction

        # Up direction scroll overflow
        # current cursor position is 0, but top position is greater than 0
        if (direction == self.up_scroll) and (self.top_line > 0 and self.cursor_y == 0):
            self.top_line += direction
            return

        # Down direction scroll overflow
        # next cursor position touch the max lines,
        # but absolute position of max lines could not touch the bottom
        if (direction == self.down_scroll) and (next_line == self.max_lines) \
                and (self.top_line + self.max_lines < self.bottom_line):
            self.top_line += direction
            return

        # Scroll up
        # current cursor position or top position is greater than 0
        if (direction == self.up_scroll) and (self.top_line > 0 or self.cursor_y > 0):
            self.cursor_y = next_line
            return

        # Scroll down
        # next cursor position is above max lines,
        # and absolute position of next cursor could not touch the bottom
        if (direction == self.down_scroll) and (next_line < self.max_lines) \
                and (self.top_line + next_line < self.bottom_line):
            self.cursor_y = next_line
            return


if __name__ == '__main__':
    app: Application = Application()
    app.set_main_window(PyHex(app.stdscr, app))
    app.run(time_wait=0)
