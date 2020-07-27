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

        # Creating the variables for the title
        self.title = "PyHex - A Python Hex Editor"

        self.title_x = int
        self.title_y = 1

    def initColors(self):
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Plaintext color
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)  # Title color

    def update(self):
        # Calculating the coordinates of the title
        self.title_x = int((self.width // 2) - (len(self.title) // 2) - len(self.title) % 2)

    def lateUpdate(self):
        # Drawing the title
        self.drawText(self.title_y, self.title_x,
                      self.title, 2)

if __name__ == '__main__':
    app: Application = Application()
    app.setMainWindow(PyHex(app.stdscr, app))
    app.run()
