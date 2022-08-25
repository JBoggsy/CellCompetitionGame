from itertools import permutations
import unicurses


ALL_COLOR_COMBINATIONS = list(permutations(
    [
        unicurses.COLOR_BLACK,
        unicurses.COLOR_WHITE,
        unicurses.COLOR_RED,
        unicurses.COLOR_GREEN,
        unicurses.COLOR_BLUE,
        unicurses.COLOR_CYAN,
        unicurses.COLOR_YELLOW,
        unicurses.COLOR_MAGENTA
    ], 2))
ALL_COLOR_COMBINATIONS.remove((unicurses.COLOR_WHITE, unicurses.COLOR_BLACK))
NUMBER_OF_COLOR_COMBOS = len(ALL_COLOR_COMBINATIONS)

MAX_INITIAL_DIVISION_THRESHOLD = 5
MUTATION_PROABILITY = 0.01
REPRESENTATION_CHANGE_PROBABILITY = 0.005
INITIAL_SPAWN_DENSITY = 0.001

COSTLY_VICTORY = 1
STANDARD_VICTORY = 2
CONQUEST_VICTORY = 3
VICTORY_TYPE = CONQUEST_VICTORY