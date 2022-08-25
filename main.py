from statistics import mean
from time import sleep, time
import sys
if sys.platform == "win32":
    import unicurses as crs
elif sys.platform == "linux":
    import curses as crs

from cell import Cell
from board import Board
from params import *
import performance


if __name__ == "__main__":
    # Curses setup
    stdscr = crs.initscr()
    crs.noecho()
    
    crs.start_color()
    print(f"Color available: {crs.has_colors()}")
    print(f"Can change colors: {crs.can_change_color()}")
    
    for i, color_combo in enumerate(ALL_COLOR_COMBINATIONS,start=1):
        crs.init_pair(i, color_combo[0], color_combo[1])

    if sys.platform == "win32":
        rows, cols = crs.getmaxyx(stdscr)
    elif sys.platform == "linux":
        rows = crs.LINES
        cols = crs.COLS
    b = Board(rows-2, cols-2, stdscr)

    tick_num = 0
    last_tick_time = time()
    if sys.platform == "win32":
        crs.nodelay(stdscr, True)
    elif sys.platform == "linux":
        stdscr.nodelay(True)
    try:
        while True:
            b.tick()

            tick_num += 1
            tick_time = time() - last_tick_time
            last_tick_time = time()
            crs.mvinsstr(0, 0, f"Tick: {tick_num}  Secs/tick: {tick_time}")
            
            key = crs.getch()
            if key == 27: break
    except KeyboardInterrupt as e:
        crs.echo()
        crs.endwin()
        for f_name, timings in performance.function_timings.items():
            print(f"{f_name}: {sum(timings)}")
        raise e

    crs.echo()
    crs.endwin()
    for f_name, timings in performance.function_timings.items():
        print(f"{f_name}: {sum(timings)}")