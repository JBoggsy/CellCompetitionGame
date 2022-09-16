from collections import defaultdict
from itertools import starmap
from random import random
from multiprocessing import Pool
import time
import sys
if sys.platform == "win32":
    import unicurses as crs
elif sys.platform == "linux":
    import curses as crs
    import _curses

from cell import Cell
from geom import *
from params import *
from performance import timer_decorator


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
        
    #@timer_decorator
    def _decision_phase(self):
        """
        invariant: any given (r, c) location contains at most one cell at the beginning of a tick
        """
        cell_nbor_pairs = []
        for (r, c), cell in self.occupied_locations.items():
            neighbor_config = self.__compute_cell_neighbors(r, c)
            cell_nbor_pairs.append((cell, neighbor_config))
        self.__serial_cell_decisions(cell_nbor_pairs)

    #@timer_decorator
    def __serial_cell_decisions(self, cell_nbor_pairs):
        decision_results = starmap(Cell.decide_cell, cell_nbor_pairs)
        for decision in decision_results:
            for result_cell, result_dest in decision:
                if len(decision) == 1:
                    self.next_occupied_locations[result_dest].insert(0, result_cell)
                else:
                    self.next_occupied_locations[result_dest].append(result_cell)

    #@timer_decorator
    def __parallel_cell_decisions(self, cell_nbor_pairs):
        with Pool(8) as p:
            decision_results = p.starmap(Cell.decide_cell, cell_nbor_pairs)
            for decision in decision_results:
                for result_cell, result_dest in decision:
                    if len(decision) == 1:
                        self.next_occupied_locations[result_dest].insert(0, result_cell)
                    else:
                        self.next_occupied_locations[result_dest].append(result_cell)

    # @timer_decorator
    def __compute_cell_neighbors(self, r, c) -> int:
        neighbor_config = []
        for nbor in range(8):
            nbor_coords =[sum(coords) for coords in zip((r, c), NBOR_ID_TO_COORD_DELTA[nbor])]
            nbor_coords[0] %= self.rows
            nbor_coords[1] %= self.rows
            nbor_coords =tuple(nbor_coords)
            if nbor_coords in self.occupied_locations.keys():
                neighbor_config.append(1)
            else:
                neighbor_config.append(0)
        return neighbor_config
    
    #@timer_decorator
    def _resolution_phase(self):
        for (r, c), cells in self.next_occupied_locations.items():
            r = r % self.rows
            c = c % self.cols
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

    #@timer_decorator
    def _draw_phase(self):
        if sys.platform == "win32":
            crs.clear()
            for (r, c), cell in self.occupied_locations.items():
                crs.mvinsstr(r+1, c+1, str(cell), crs.color_pair(cell.color))
            crs.border()
            crs.move(0,0)
            crs.refresh()
        elif sys.platform == "linux":
            self.stdscr.clear()
            self.stdscr.refresh()
            for (r, c), cell in self.occupied_locations.items():
                try:
                    self.stdscr.insstr(min(max(0,r),self.rows), min(max(0,c),self.cols), str(cell), crs.color_pair(cell.color))
                except _curses.error as e:
                    print(r,c,cell, crs.color_pair(cell.color))
                    raise e
            self.stdscr.border()
            self.stdscr.move(0,0)
            self.stdscr.refresh()
        # with open(f"log-{time.time()}.txt", "a") as outfile:
        #     outfile.write(repr(self))


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

    def __repr__(self) -> str:
        ret_str = f"{{'rows': {self.rows},'cols': {self.cols},"
        for loc, cell in self.occupied_locations.items():
            ret_str += f"'{loc}': {repr(cell)},"
        ret_str += "}"
        return ret_str

