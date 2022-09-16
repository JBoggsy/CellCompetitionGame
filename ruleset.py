from params import *

import numpy as np


class Ruleset(object):
    def __init__(self, source=None) -> None:
        if source:
            self.weights = source.weights.copy()
            self.division_base = source.division_base
            self.mutate()
        else:
            destination_weights = np.random.normal(scale=INITIAL_DESTINATION_SIGMA, size=64).reshape((8,8))
            division_weights = np.random.normal(loc=INITIAL_DIVISION_WEIGHTS_MU, scale=INITIAL_DIVISION_WEIGHTS_SIGMA, size=8).reshape(1,8)
            self.weights = np.concatenate((destination_weights, division_weights))
            self.division_base = np.random.normal(INITIAL_DIVISION_BASE_MU, INITIAL_DIVISION_BASE_SIGMA, 1)[0]

    def compute(self, nbor_vector):
        result_vector = np.dot(self.weights, nbor_vector)
        divide_thresh = result_vector[-1] + self.division_base
        destinations = result_vector[:-1].argsort()[-2:]
        return (divide_thresh, destinations)

    def mutate(self):
        mutation_matrix = np.random.normal(scale=MUTATION_SIGMA, size=9*8).reshape((9,8))
        self.weights += mutation_matrix

    def __call__(self, nbor_vector:list):
        return self.compute(nbor_vector=nbor_vector)
    
    def __str__(self) -> str:
        ret_str = ""
        for row in self.weights:
            row_str = " ".join([f"{d:^+3.3f}" for d in row])
            ret_str += row_str + "\n"
        return ret_str

    def __repr__(self) -> str:
        return repr(self.weights)


if __name__ == "__main__":
    test_rset = Ruleset()
    print(str(test_rset))
    print(test_rset(np.random.randint(0, 2, 8)))