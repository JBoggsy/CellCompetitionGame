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

INITIAL_SPAWN_DENSITY = 0.1
INITIAL_DESTINATION_SIGMA = 1
INITIAL_DIVISION_BASE_MU = 10
INITIAL_DIVISION_BASE_SIGMA = 5
INITIAL_DIVISION_WEIGHTS_MU = 0
INITIAL_DIVISION_WEIGHTS_SIGMA = 2

MUTATION_SIGMA = 0.001
REPRESENTATION_CHANGE_PROBABILITY = 0.005


COSTLY_VICTORY = 1
STANDARD_VICTORY = 2
CONQUEST_VICTORY = 3
VICTORY_TYPE = CONQUEST_VICTORY
