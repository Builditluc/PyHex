""""
Simple classes for the PyHex Window and Application
"""

import curses
import time


class Window:
    """
    Simple class for a curses Window
    """
    def __init__(self, stdscr, application):
        super(__class__, self).__init__()

        # Saves the Screen of the Window and the parent application in a variable
        self.stdscr: curses.window = stdscr
        self.application: Application = application

        # Creating the variables of the size of the Window
        self.width = int
        self.height = int

        # Creating the variable for the Keyinput
        self.key_pressed = int

    def init_colors(self):
        """
        Function for initiating the colors of a Window.
        Must be called manually.
        """

    def update(self):
        """
        This function will be called every time the Window updates.
        Mostly, you will do calculations of coordinates for the drawing in here.
        """

    def late_update(self):
        """
        This function will be called every time after the update function.
        Mostly, you will draw things on the screen here.
        """

    def check_keys(self):
        """
        This function will be called every frame.
        """

    def window_update(self):
        """
        This function will be called from the Application and calls
        functions like update or lateUpdate.
        Do not change anything in here!
        """
        self.height, self.width = self.stdscr.getmaxyx()
        self.key_pressed = self.stdscr.getch()
        self.check_keys()

        self.update()

        # Clear the Screen
        self.stdscr.erase()

        self.late_update()

        # Refreshing the Screen at the end of the Frame
        self._update_screen()

    def _update_screen(self):
        """
        This function just refreshes the Screen.
        """
        self.stdscr.refresh()

    def draw_text(self, y_coord, x_coord, text, color_code):
        """
        This function draws text on the screen
        :param y_coord: The y-Coordinate
        :param x_coord: The x_coord-Coordinate
        :param text: The text that will be drawn at the Coordinates
        :param color_code: The Code of the Color Pair you want to use for the text
        """
        self.stdscr.attron(curses.A_BOLD)
        self.stdscr.attron(curses.color_pair(color_code))

        self.stdscr.addstr(y_coord, x_coord, text)

        self.stdscr.attroff(curses.A_BOLD)
        self.stdscr.attroff(curses.color_pair(color_code))

    @staticmethod
    def set_cursor_state(state: int):
        """
        Changes the Cursor in the window
        :param state: 0 - Hides the Cursor
        :param state: 1 - Shows the Cursor
        :param state: 2 - Makes the Cursor highly visible
        """
        curses.curs_set(state)

    def exit(self):
        """
        This function will be called, when the program closes
        """

class Application:
    """
    Simple class for a application managing a window
    """
    colormode: bool
    no_delay: bool

    def __init__(self):
        super(__class__, self).__init__()
        time.sleep(0.5)

        # First, initiating the Screen and defining a variable for the MainWindow of the Application
        self.stdscr = curses.initscr()
        self.stdscr.keypad(True)
        self.window = None

        curses.noecho()
        curses.cbreak()

        # Check, if the terminal supports colors and activates the NoDelay mode, if enabled
        self.colormode = curses.has_colors()
        self.no_delay = True
        if self.no_delay:
            self.stdscr.nodelay(True)

    def set_main_window(self, window: Window):
        """
        This function sets the MainWindow of the application
        :param window: The Window
        """
        self.window = window

    def run(self, time_wait=0.015):
        """
        This function starts the Programm
        :param time_wait: Time to wait between the frame updates
        """
        while True:
            self.window.window_update()
            time.sleep(time_wait)
