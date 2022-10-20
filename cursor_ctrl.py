import sched
import threading
import time


class CursorCtrl:
    def __init__(self):
        self.cursor_on = True
        self.scheduler = sched.scheduler(time.time, time.sleep)

    def flash_cursor(self, str):
        if self.cursor_on:
            print('\033[?25l', end='', flush=True)
            self.cursor_on = not self.cursor_on
        else:
            print('\033[?25h', end='', flush=True)
            self.cursor_on = not self.cursor_on

        self.scheduler.enter(0.5, 2, self.flash_cursor, ('',))

    def start_cur_flashing(self):
        # Schedule the flash_cursor function as an event
        self.scheduler.enter(0.5, 2, self.flash_cursor, ('',))
        # Start a thread to run the events
        thr = threading.Thread(target=self.scheduler.run)
        thr.start()
        return thr

    def stop_cur_flashing(self, thr):
        self.scheduler.cancel(self.scheduler.queue[0])
        print('\033[?25h', end="")  # Turn the cursor back on
        # Terminate the thread when tasks finish
        thr.join()


""" Set of functions to move the cursor around """


def move_cur_left(n=1):
    """Move the cursor left"""
    print(f"\033[{n}D")


def move_cur_right(n=1):
    """Move the cursor one position to the right"""
    print(f"\033[{n}C")


def move_cur_up(n=1):
    """Move the cursor up one line (without affecting its horizontal position)"""
    print(f"\033[{n}A")


def move_cur_down(n=1):
    """Move the cursor down one line (without affecting its horizontal position)"""
    print(f"\033[{n}B")


def move_cur_home():
    """Move the cursor to 0,0"""
    print("\033[H")


def move_cur_line_xy(line, col):
    """Move the cursor to xy"""
    print(f"\033[{line};{col}H")
