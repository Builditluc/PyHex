#!/usr/bin/env python3.8
"""
PyHex is a simple python Hex editor
"""

import curses
import curses.ascii
import sys
import os
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

        self.special_characters = ["\a", "\b", "\f", "\n", "\r", "\t", "\v", "\x00"]

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
                try:
                    ascii_object = byte_object.decode("ascii")
                except UnicodeDecodeError:
                    ascii_object = "."

                # Replace the char with a dot if it's a special character
                if ascii_object in self.special_characters:
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
    # pylint: disable=too-many-statements
    # pylint: disable=no-member
    def __init__(self, *args, **kwargs):
        super(__class__, self).__init__(*args, **kwargs)
        self.init_colors()

        # Hiding the Cursor
        self.set_cursor_state(0)
        self.columns = 16
        self.last_line = curses.LINES - 2

        self.changed = False
        self.save_dialog = False

        self.max_lines = self.last_line - 3  # Max number of lines on the screen
        self.top_line = self.bottom_line = 0  # The lines at the top and the bottom of the screen
        self.edit_lines = self.encoded_lines = self.decoded_lines = self.offset_lines = []

        self.cursor_y = self.cursor_x = 0  # The coords of the cursor
        self.content_pos_y = self.content_pos_x = 0  # The coords of the cursor in the Hex Array

        self.up_scroll = -1
        self.down_scroll = 1

        self.left_scroll = -1
        self.right_scroll = 1

        # All the keys that can be written to a byte
        self.edit_keys = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
                          "a", "b", "c", "d", "e", "f"]

        for _i, key in enumerate(self.edit_keys):
            self.edit_keys[_i] = ord(str(key))

        # The position of the cursor in a byte (0 or 1)
        self.edited_position = 0

        # Creating the variables for the title
        self.title = "PyHex - A Python Hex Editor"

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
        self.encoded_title_x = 13
        self.encoded_title_y = 1

        self.encoded_text_x = 13
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

        # Creating the variables for the Status bar
        self._status_bar_text = "{}".format(os.path.basename(self.filename))
        self.status_bar_text = ""
        self.status_bar_color = 3
        self.get_status_bar_text = lambda: self._status_bar_text + self.status_bar_text

        # Creating the array for the edited bytes
        self.edited_array = []
        for line in self.file.hex_array:
            edited_line = ["--"] * len(line)
            self.edited_array.append(edited_line)

        # Decode the File into ascii
        self.decoded_text = self.file.decode_hex()

        # Calculate the bottom line
        self.bottom_line = len(self.file.hex_array)

    def init_colors(self):
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Plaintext color
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)  # Title color
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Selected color
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)  # Edited color
        curses.init_pair(5, curses.COLOR_RED, curses.COLOR_WHITE)  # Selected-Edited color

    def check_keys(self):
        if self.save_dialog:
            if self.key_pressed == ord("y"):
                self.save()
            if self.key_pressed == ord("n"):
                self.changed = self.save_dialog = False
                self.exit()
            if self.key_pressed == curses.ascii.ESC:
                self.save_dialog, self.status_bar_text = False, ""
            return

        if self.key_pressed == curses.ascii.ESC or self.key_pressed == ord("q"):
            self.exit()

        if self.key_pressed == curses.KEY_UP:
            self.scroll_vertically(self.up_scroll)
        elif self.key_pressed == curses.KEY_DOWN:
            self.scroll_vertically(self.down_scroll)

        if self.key_pressed == curses.KEY_LEFT:
            self.scroll_horizontally(self.left_scroll)
        elif self.key_pressed == curses.KEY_RIGHT:
            self.scroll_horizontally(self.right_scroll)

        if self.key_pressed in self.edit_keys:
            char = chr(self.key_pressed)
            self.edit(char, self.content_pos_y, self.content_pos_x)

        if self.key_pressed == curses.ascii.BS:
            self.clear_edit(self.content_pos_y, self.content_pos_x)

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
        self.decoded_title_x = self.encoded_title_x + len(self.encoded_title) + 2
        self.decoded_text_x = self.decoded_title_x

        # Calculating the offset
        total_lines = len(self.file.hex_array)
        self.offset_text = []
        for i in range(0, total_lines):
            offset = hex(i * self.columns).replace("x", "").upper()
            offset = "0" * (self.offset_len - len(str(offset))) + str(offset)
            self.offset_text.append(offset)

        self.encoded_lines = self.file.hex_array[self.top_line:self.top_line + self.max_lines]
        self.decoded_lines = self.decoded_text[self.top_line:self.top_line + self.max_lines]
        self.edit_lines = self.edited_array[self.top_line:self.top_line + self.max_lines]
        self.offset_lines = self.offset_text[self.top_line:self.top_line + self.max_lines]

        # Calculate the Status Bar Text
        if self.changed:
            self.status_bar_text = "* "
        else:
            self.status_bar_text = ""

        if self.save_dialog:
            self.status_bar_text = " | Would you like to save your file? y,n,esc"

    def late_update(self):
        self._draw_box()
        self._draw_titles()
        self._draw_offset()
        self._draw_encoded()
        self._draw_decoded()
        self._draw_status_bar()

    def exit(self):
        if self.changed:
            self.save_dialog = True
            return

        curses.endwin()
        sys.exit()

    def _draw_box(self):
        # Draw the Horizontal lines
        self.draw_text(self.offset_text_y, self.offset_text_x - 1,
                       "\u250C" + "\u2500" * (self.offset_len + (self.columns * 4 + 5)) +
                       "\u2510", 1)
        self.draw_text(self.offset_text_y, self.encoded_text_x - 2, "\u252C", 1)
        self.draw_text(self.offset_text_y, self.decoded_text_x - 2, "\u252C", 1)

        self.draw_text(self.last_line, self.offset_text_x - 1,
                       "\u2514" + "\u2500" * (self.offset_len + (self.columns * 4 + 5)) +
                       "\u2518", 1)
        self.draw_text(self.last_line, self.decoded_text_x - 2, "\u2534", 1)
        self.draw_text(self.last_line, self.encoded_text_x - 2, "\u2534", 1)

        # Draw the Vertical lines
        for i in range(self.offset_text_y + 1, self.last_line):
            self.draw_text(i, self.offset_text_x - 1, "\u2502" + " " * (self.offset_len + 1) +
                           "\u2502" + " " * (self.columns * 3 + 1) + "\u2502" +
                           " " * (self.columns + 1) + "\u2502", 1)

    def _draw_titles(self):

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

    def _draw_offset(self):
        y_coord = self.offset_text_y + 1
        x_coord = self.offset_text_x

        for offset in self.offset_lines:
            self.draw_text(y_coord, x_coord, offset, 1)
            y_coord += 1

    def _draw_encoded(self):
        y_coord = self.encoded_text_y + 1
        x_coord = self.encoded_text_x
        x_offset = 0

        for _y, line in enumerate(self.encoded_lines):
            for _x, byte in enumerate(line):
                edited_color = 4
                normal_color = 1

                if _y == self.cursor_y and _x == self.cursor_x:
                    edited_color = 5
                    normal_color = 3

                if (self.edit_lines[_y][_x][:1] != "-") and (self.edit_lines[_y][_x][1:] != "-"):
                    self.draw_text(y_coord, x_coord + x_offset,
                                   self.edit_lines[_y][_x], edited_color)
                elif self.edit_lines[_y][_x][1:] != "-":
                    self.draw_text(y_coord, x_coord + x_offset,
                                   self.edit_lines[_y][_x][1:] + byte[:1], edited_color)
                elif self.edit_lines[_y][_x][:1] != "-":
                    self.draw_text(y_coord, x_coord + x_offset,
                                   self.edit_lines[_y][_x][:1] + byte[1:], edited_color)
                elif self.edit_lines[_y][_x] == "--":
                    self.draw_text(y_coord, x_coord + x_offset, byte, normal_color)
                x_offset += 3
            x_offset = 0
            y_coord += 1

    def _draw_decoded(self):
        y_coord = self.decoded_text_y + 1
        x_coord = self.decoded_text_x

        for _y, line in enumerate(self.decoded_lines):
            x_offset = 0
            for _x, char in enumerate(line):
                edited_color = 4
                normal_color = 1
                edited = False

                if _y == self.cursor_y and _x == self.cursor_x:
                    edited_color = 5
                    normal_color = 3

                if self.edit_lines[_y][_x] == "--":
                    self.draw_text(y_coord, x_coord + x_offset, char, normal_color)
                elif self.edit_lines[_y][_x][:1] == "-":
                    hex_object = self.encoded_lines[_y][_x][:1] + self.edit_lines[_y][_x][1:]
                    edited = True
                elif self.edit_lines[_y][_x][1:] == "-":
                    hex_object = self.edit_lines[_y][_x][:1] + self.encoded_lines[_y][_x][:1]
                    edited = True
                else:
                    hex_object = self.edit_lines[_y][_x]
                    edited = True

                if edited:
                    # Convert the hex byte into a normal byte
                    byte_object = bytes.fromhex(hex_object)

                    # Convert the byte into ascii
                    try:
                        ascii_object = byte_object.decode("ascii")
                    except UnicodeDecodeError:
                        ascii_object = "."

                    # Replace the char with a dot if it's a special character
                    if ascii_object in self.file.special_characters:
                        ascii_object = "."

                    self.draw_text(y_coord, x_coord + x_offset, ascii_object, edited_color)
                x_offset += 1
            y_coord += 1

    def _draw_status_bar(self):
        self.draw_text(self.last_line + 1, 0, " "*(self.width-1), self.status_bar_color)
        self.draw_text(self.last_line + 1, 0, self.get_status_bar_text(), self.status_bar_color)

    def scroll_horizontally(self, direction):
        """
        Moves the cursor to the left/right using the left/right arrow keys
        :param direction: The direction of the Scrolling (Left or Right)
        """
        # next cursor position after scrolling
        next_position = self.cursor_x + direction

        # When scroll left or right, reset the edited position
        if direction in (self.left_scroll, self.right_scroll):
            self.edited_position = 0

        # Scroll left
        # current cursor position or left position is greater or equal than 0
        if (direction == self.left_scroll) and (self.cursor_x >= 0) and (next_position >= 0):
            self.cursor_x = next_position
            self.content_pos_x += direction
            return

        # Scroll right
        # absolute position of next cursor is not the right edge
        if (direction == self.right_scroll) and (next_position < self.columns):
            self.cursor_x = next_position
            self.content_pos_x += direction
            return

        # Left overflow
        # next cursor position is smaller than 0 and the current line is not the top
        if (direction == self.left_scroll) and (next_position < 0 < self.content_pos_y):
            self.cursor_x = self.columns - 1
            self.content_pos_x = self.columns - 1
            self.scroll_vertically(self.up_scroll)
            return

        # Right overflow
        # next cursor position is over the right edge
        if (direction == self.right_scroll) and (next_position == self.columns):
            self.cursor_x = 0
            self.content_pos_x = 0
            self.scroll_vertically(self.down_scroll)
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
            self.content_pos_y += direction
            return

        # Down direction scroll overflow
        # next cursor position touch the max lines,
        # but absolute position of max lines could not touch the bottom
        if (direction == self.down_scroll) and (next_line == self.max_lines) \
                and (self.top_line + self.max_lines < self.bottom_line):
            self.top_line += direction
            self.content_pos_y += direction
            return

        # Scroll up
        # current cursor position or top position is greater than 0
        if (direction == self.up_scroll) and (self.top_line > 0 or self.cursor_y > 0):
            self.cursor_y = next_line
            self.content_pos_y += direction
            return

        # Scroll down
        # next cursor position is above max lines,
        # and absolute position of next cursor could not touch the bottom
        if (direction == self.down_scroll) and (next_line < self.max_lines) \
                and (self.top_line + next_line < self.bottom_line):
            self.cursor_y = next_line
            self.content_pos_y += direction
            return

    def edit(self, char, cursor_y, cursor_x):
        """
        Changes one character of a byte
        :param cursor_y: The y coordinate of the cursor in the array
        :param cursor_x: The x coordinate of the cursor in the array
        """
        # If the character is a letter, make it upper
        if char.isalpha():
            char = char.upper()

        # Add the byte to the edited array
        for _y, line in enumerate(self.edited_array):
            for _x in range(0, len(line)):
                if _y == cursor_y and _x == cursor_x:
                    if self.edited_position == 0:
                        self.edited_array[_y][_x] = str(char) + self.edited_array[_y][_x][1:]
                        self.edited_position = 1
                        self.changed = True
                        return

                    if self.edited_position == 1:
                        self.edited_array[_y][_x] = self.edited_array[_y][_x][:1] + str(char)
                        self.edited_position = 0
                        self.changed = True
                        self.scroll_horizontally(self.right_scroll)
                        return

    def clear_edit(self, cursor_y, cursor_x):
        """
        Removes the edit of a byte
        :param cursor_y: The y coordinate of the cursor in the array
        :param cursor_x: The x coordinate of the cursor in the array
        """
        no_edit = True
        # Clear the byte in the edited array
        for _y, line in enumerate(self.edited_array):
            for _x, byte in enumerate(line):
                if _y == cursor_y and _x == cursor_x:
                    self.edited_array[_y][_x] = "--"

                    # When the byte was cleared, move the cursor to the left
                    self.scroll_horizontally(self.left_scroll)
                    self.edited_position = 0

                if byte != "--":
                    no_edit = False

        if no_edit:
            self.changed = False

    def save(self):
        """
        Saves the content to the opened file
        """
        file_content = b''

        for _y, line in enumerate(self.file.hex_array):
            for _x, byte in enumerate(line):
                edited_byte = self.edited_array[_y][_x]
                if edited_byte == "--":
                    hex_byte = byte
                elif edited_byte[:1] == "-":
                    hex_byte = byte[:1] + edited_byte[1:]
                elif edited_byte[1:] == "-":
                    hex_byte = edited_byte[:1] + byte[1:]
                else:
                    hex_byte = edited_byte
                file_content += bytes.fromhex(hex_byte)

        with open(self.filename, "wb") as _f:
            _f.write(file_content)
            _f.close()

        self.changed = False
        self.save_dialog = False
        self.exit()

if __name__ == '__main__':
    app: Application = Application()
    app.set_main_window(PyHex(app.stdscr, app))
    app.run(time_wait=0)
