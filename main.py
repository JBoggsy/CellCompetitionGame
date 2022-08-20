from statistics import mean
from time import sleep, time

from cell import Cell
from board import Board
from params import *
import performance

import unicurses


if __name__ == "__main__":
    # Curses setup
    stdscr = unicurses.initscr()
    unicurses.noecho()
    
    unicurses.start_color()
    print(f"Color available: {unicurses.has_colors()}")
    print(f"Can change colors: {unicurses.can_change_color()}")
    
    for i, color_combo in enumerate(ALL_COLOR_COMBINATIONS,start=1):
        unicurses.init_pair(i, color_combo[0], color_combo[1])
    rows, cols = unicurses.getmaxyx(stdscr)
    b = Board(rows-2, cols-2, stdscr)

    tick_num = 0
    last_tick_time = time()
    unicurses.nodelay(stdscr, True)
    try:
        while True:
            b.tick()

            tick_num += 1
            tick_time = time() - last_tick_time
            last_tick_time = time()
            unicurses.mvinsstr(0, 0, f"Tick: {tick_num}  Secs/tick: {tick_time}")
            
            key = unicurses.getch()
            if key == 27: break
    except KeyboardInterrupt as e:
        unicurses.echo()
        for f_name, timings in performance.function_timings.items():
            print(f"{f_name}: {sum(timings)}")
        raise e

    unicurses.echo()
    for f_name, timings in performance.function_timings.items():
        print(f"{f_name}: {sum(timings)}")