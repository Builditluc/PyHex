# PyHex
# Made by Builditluc

import curses, time


class Window(object):
    def __init__(self, stdscr, application):
        super(__class__, self).__init__()

        # Saves the Screen of the Window and the parent application in a variable
        self.stdscr: curses.window = stdscr
        self.application: Application = application

        # Creating the variables of the size of the Window
        self.width = int
        self.height = int

        # Creating the variable for the Keyinput
        self.keyPressed = int

    def initColors(self):
        """
        Function for initiating the colors of a Window.
        Must be called manually.
        """
        pass

    def update(self):
        """
        This function will be called every time the Window updates.
        Mostly, you will do calculations of coordinates for the drawing in here.
        """
        pass

    def lateUpdate(self):
        """
        This function will be called every time after the update function.
        Mostly, you will draw things on the screen here.
        """
        pass

    def _update(self):
        """
        This function will be called from the Application and calls
        functions like update or lateUpdate.
        Do not change anything in here!
        """
        self.height, self.width = self.stdscr.getmaxyx()
        self.keyPressed = self.stdscr.getch()

        self.update()
        self.lateUpdate()

        # Refreshing the Screen at the end of the Frame
        self._updateScreen()

    def _updateScreen(self):
        """
        This function just refreshes the Screen.
        """
        self.stdscr.refresh()

    def drawText(self, y, x, text, color_code):
        """
        This function draws text on the screen
        :param y: The y-Coordinate
        :param x: The x-Coordinate
        :param text: The text that will be drawn at the Coordinates
        :param color_code: The Code of the Color Pair you want to use for the text
        """
        self.stdscr.attron(curses.A_BOLD)
        self.stdscr.attron(curses.color_pair(color_code))

        self.stdscr.addstr(y, x, text)

        self.stdscr.attroff(curses.A_BOLD)
        self.stdscr.attroff(curses.color_pair(color_code))

    def setCursorState(self, state: int):
        """
        Changes the Cursor in the window
        :param state: 0 - Hides the Cursor
        :param state: 1 - Shows the Cursor
        :param state: 2 - Makes the Cursor highly visible
        """
        curses.curs_set(state)


class Application(object):
    COLORMODE: bool
    NODELAY: bool

    def __init__(self):
        super(__class__, self).__init__()
        time.sleep(0.5)

        # First, initiating the Screen and defining a variable for the MainWindow of the Application
        self.stdscr = curses.initscr()
        self.window = None

        # Check, if the terminal supports colors and activates the NoDelay mode, if enabled
        self.COLORMODE = curses.has_colors()
        self.NODELAY = True
        if self.NODELAY:
            self.stdscr.nodelay(True)

    def setMainWindow(self, window: Window):
        """
        This function sets the MainWindow of the application
        :param window: The Window
        """
        self.window = window

    def run(self, time_wait=0.15):
        """
        This function starts the Programm
        :param time_wait: Time to wait between the frame updates
        """
        while True:
            self.window._update()
            time.sleep(time_wait)
