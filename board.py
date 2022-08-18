from collections import defaultdict
from random import random

import unicurses

from cell import Cell
from geom import *
from params import *


class Board(object):
    def __init__(self, rows:int, cols:int, stdscr) -> None:
        self.rows = rows
        self.cols = cols
        self.stdscr = stdscr
        self.occupied_locations = {}  # maps pairs of (r, c) coordinates onto `Cell`s
        self.next_occupied_locations = defaultdict(list)  # maps pairs of (r, c) coordinates onto lists of `Cell`s


        for r in range(self.rows):
            for c in range(self.cols):
                if random() < INITIAL_SPAWN_DENSITY:
                    self.occupied_locations[(r,c)] = Cell((r, c))
        
    def tick(self) -> str:
        self._decision_phase()
        self.occupied_locations.clear()
        self._resolution_phase()
        self._draw_phase()
        
        # print(str(self))

    def _decision_phase(self):
        """
        invariant: any given (r, c) location contains at most one cell at the beginning of a tick
        """
        for (r, c), cell in self.occupied_locations.items():
            neighbor_config = 0
            for nbor in range(8):
                nbor_coords = tuple([sum(coords) for coords in zip((r, c), NBOR_ID_TO_COORD_DELTA[nbor])])
                if nbor_coords in self.occupied_locations.keys():
                    neighbor_config += 2**nbor
            decision_results = cell.decide(neighbor_config)
            for result_cell, result_dest in decision_results:
                if len(decision_results) == 1:
                    self.next_occupied_locations[result_dest].insert(0, result_cell)
                else:
                    self.next_occupied_locations[result_dest].append(result_cell)
    
    def _resolution_phase(self):
        for (r, c), cells in self.next_occupied_locations.items():
            if not ((0 <= r < self.rows) or (0 <= c < self.cols)):
                continue
            while len(cells) > 1:
                cell_a = cells.pop()
                cell_b = cells.pop()
                victor = max(cell_a, cell_b)
                loser = min(cell_a, cell_b)
                if VICTORY_TYPE == COSTLY_VICTORY:
                    victor.energy_level -= loser.energy_level
                elif VICTORY_TYPE == CONQUEST_VICTORY:
                    victor.energy_level += loser.energy_level
                cells.append(victor)
            if cells[0].energy_level > 0:
                self.occupied_locations[(r, c)] = cells[0]
        self.next_occupied_locations.clear()

    def _draw_phase(self):
        unicurses.clear()
        unicurses.refresh()
        for (r, c), cell in self.occupied_locations.items():
            unicurses.mvinsstr(r+1, c+1, str(cell), unicurses.color_pair(cell.color))
        unicurses.border()
        unicurses.move(0,0)
        unicurses.refresh()

    def __str__(self) -> str:
        ret_str = ""
        for r in range(self.rows):
            row_str = ""
            for c in range(self.cols):
                if (r, c) in self.occupied_locations:
                    row_str += str(self.occupied_locations[(r,c)])
                else:
                    row_str += " "
            row_str += "\n"
            ret_str += row_str
        return ret_str

