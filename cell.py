from copy import deepcopy
from random import randint, randrange, sample, random

from params import *
from geom import *

class Cell(object):
    NEXT_CELL_CHAR = 33
    
    def __init__(self, location:tuple, initial_energy:int=1, ruleset:dict=None) -> None:
        self.location = location
        self.energy_level = initial_energy
        self.ruleset = ruleset
        self.representation = chr(Cell.NEXT_CELL_CHAR)

        Cell.NEXT_CELL_CHAR = Cell.NEXT_CELL_CHAR + 1
        if Cell.NEXT_CELL_CHAR > 254: Cell.NEXT_CELL_CHAR = 33

        if self.ruleset:
            self.mutate()
        else:
            self.gen_ruleset()

    def decide(self, neighbors:int) -> list:
        threshold, (dest_a, dest_b) = self.ruleset[neighbors]
        dest_a = tuple([sum(coords) for coords in zip(self.location, NBOR_ID_TO_COORD_DELTA[dest_a])])
        dest_b = tuple([sum(coords) for coords in zip(self.location, NBOR_ID_TO_COORD_DELTA[dest_b])])
        if self.energy_level <= 0:
            results = []
        elif self.energy_level >= threshold:
            child_energy_level = self.energy_level//2
            child_a = Cell(dest_a, child_energy_level, deepcopy(self.ruleset))
            child_b = Cell(dest_b, child_energy_level, deepcopy(self.ruleset))
            results = [(child_a, dest_a), (child_b, dest_b)]
        else:
            self.energy_level += 1
            results = [(self, self.location),]
        return results

    def gen_ruleset(self):
        self.ruleset = dict()
        for neighbor_config in range(256):
            threshold = randrange(2, MAX_INITIAL_DIVISION_THRESHOLD)
            destination_a, destination_b = sample(range(8), k=2)
            self.ruleset[neighbor_config] = [threshold, [destination_a, destination_b]]

    def mutate(self):
        for neighbor_config in self.ruleset:
            if random() < MUTATION_PROABILITY:
                self._mutate_rule(neighbor_config)

    def _mutate_rule(self, neighbor_config):
        mutate_threshold = random() < 0.5
        if mutate_threshold:
            increment = random() < 0.5
            if increment:
                self.ruleset[neighbor_config][0] += 1
            else:
                self.ruleset[neighbor_config][0] -= 1
        else:
            dest_idx = randrange(0, 2)
            clockwise = random() < 0.5
            if clockwise:
                self.ruleset[neighbor_config][1][dest_idx] = (self.ruleset[neighbor_config][1][dest_idx] + 1) % 8
            else:
                self.ruleset[neighbor_config][1][dest_idx] = (self.ruleset[neighbor_config][1][dest_idx] - 1) % 8

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