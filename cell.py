from copy import deepcopy
from random import randint, randrange, sample, random

import numpy as np

from params import *
from geom import *
from ruleset import Ruleset
from performance import timer_decorator


class Cell(object):
    NEXT_CELL_CHAR = 33
    NEXT_CELL_COLOR = 0
    
    def __init__(self, location:tuple, initial_energy:int=1, ruleset:Ruleset=None, representation=None, color=None) -> None:
        self.location = location
        self.energy_level = initial_energy
        self.ruleset = Ruleset(ruleset)
        
        if representation:
            if random() < REPRESENTATION_CHANGE_PROBABILITY:
                self.representation = Cell.get_new_cell_repr()
            else:
                self.representation = representation
        else:
            self.representation = Cell.get_new_cell_repr()

        if color:
            self.color = color
        else:
            self.color = Cell.get_new_color()

    # @timer_decorator
    def decide(self, neighbors:list) -> list:
        threshold, (dest_a, dest_b) = self.ruleset(neighbors)
        dest_a = tuple([sum(coords) for coords in zip(self.location, NBOR_ID_TO_COORD_DELTA[dest_a])])
        dest_b = tuple([sum(coords) for coords in zip(self.location, NBOR_ID_TO_COORD_DELTA[dest_b])])
        if self.energy_level <= 0:
            results = []
        elif self.energy_level >= threshold:
            child_a = self.create_child(dest_a)
            child_b = self.create_child(dest_b)
            results = [(child_a, dest_a), (child_b, dest_b)]
        else:
            self.energy_level += 1
            results = [(self, self.location),]
        return results

    # @timer_decorator
    def create_child(self, dest):
        child = Cell(dest, self.energy_level//2, self.ruleset, self.representation, self.color)
        return child

    def __gt__(self, other) -> bool:
        assert type(other) is Cell
        return self.energy_level > other.energy_level

    def __ge__(self, other):
        return self.energy_level >= other.energy_level

    def __lt__(self, other):
        return self.energy_level < other.energy_level

    def __le__(self, other):
        return self.energy_level <= other.energy_level

    def __eq__(self, other) -> bool:
        return self.energy_level == other.energy_level

    def __str__(self) -> str:
        return self.representation

    def get_new_cell_repr():
        new_repr = chr(Cell.NEXT_CELL_CHAR)
        Cell.NEXT_CELL_CHAR += + 1
        if Cell.NEXT_CELL_CHAR > 254: Cell.NEXT_CELL_CHAR = 33
        return new_repr
    
    def get_new_color():
        new_color = Cell.NEXT_CELL_COLOR
        Cell.NEXT_CELL_COLOR += 1
        Cell.NEXT_CELL_COLOR = Cell.NEXT_CELL_COLOR % NUMBER_OF_COLOR_COMBOS
        return new_color
        
    def decide_cell(cell, neighbor_config):
        return cell.decide(neighbor_config)