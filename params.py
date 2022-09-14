from itertools import permutations
import sys
if sys.platform == "win32":
    import unicurses as crs
elif sys.platform == "linux":
    import curses as crs

ALL_COLOR_COMBINATIONS = list(permutations(
    [
        crs.COLOR_BLACK,
        crs.COLOR_WHITE,
        crs.COLOR_RED,
        crs.COLOR_GREEN,
        crs.COLOR_BLUE,
        crs.COLOR_CYAN,
        crs.COLOR_YELLOW,
        crs.COLOR_MAGENTA
    ], 2))
ALL_COLOR_COMBINATIONS.remove((crs.COLOR_WHITE, crs.COLOR_BLACK))
NUMBER_OF_COLOR_COMBOS = len(ALL_COLOR_COMBINATIONS)

MAX_INITIAL_DIVISION_THRESHOLD = 15
MUTATION_PROABILITY = 0.01
REPRESENTATION_CHANGE_PROBABILITY = 0.005
INITIAL_SPAWN_DENSITY = 0.1

COSTLY_VICTORY = 1
STANDARD_VICTORY = 2
CONQUEST_VICTORY = 3
VICTORY_TYPE = STANDARD_VICTORY
