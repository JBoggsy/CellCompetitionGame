# Cell Competition Game
This "game" is a spinoff of Conway's famous Game of Life, in which a simple rule dictates whether 
each cell on a gridded game board is "alive" or "dead" in the next iteration. The next state of
each cell is decided by tallying the number of living neighbors each cell has, then checking the
rule to see whether the cell should live or die. This game takes that concept several steps further
by treating the cells not as fixed locations on the grid but as independent entities, whose actions
are dictated by a ruleset unique to that cell. Rather than living or dying merely in accordance 
with the number of living neighbors it has, each cell can choose either to continue living or to
"divide" splitting itself into two new cells. If the cell chooses to remain alive, it accumulates
energy; should it divide, the old cell dies and is removed from the board, and two new cells are
created in neighboring locations, each with half the parent cell's energy. 

## Cell Behavior
At the beginning of each tick, the cell has two choices:

1. Continue living and maintain its current position, while increasing its energy level by one.
2. Destroy itself, leaving its current location empty and creating two children in two respective
neighboring locations, each of which will have half the cell's current energy level.

Which choice the cell makes, that is, whether it persists or divides, is determined by the cell's
**behavioral ruleset (BR)**. The BR determines which action is taken based on two factors: the
absence or presence of another living cell in each of the eight locations neighboring the cell and
the cell's energy level. Since each of the each neighboring locations can either have a living cell
or be empty, that presents 2^8 = 256 different neighborly configurations. The BR lists two things
for each of these possible configurations:

1. the energy level threshold at (or above) which the cell will divide rather than persist, and
2. which two neighboring locations will be the destination for the two new cells created by a
division, should the cell have enough energy to divide.

Thus, at each tick each living cell will consult its BR using its perception of its eight immediate
neighbors and decide whether to persist for another tick, thereby accumulating more energy, or 
instead to divide, destroying itself but spawning two children. Should a cell decide to divide, it
then consults its BR for which two neighboring locations it will try and divide into. 

## Cell Division
The process of cell division is relatively simple. As explained above, at the end of a tick in 
which a cell chooses to divide, that cell is destroyed and two new cells are created in the two
locations defined by the parent cell's behavioral ruleset. These new cells are each created with
have half (rounded down) of the parent cell's original energy level, *as well as* a copy their 
parent's BR. After each cell is initially created, it undergoes **mutation**, in which each of the
256 rules in the cell's BR have a chance to be slightly altered. A mutation to a rule can take one
of two forms:

1. the energy threshold for division under that neighborly configuration is increased or decreased
by one (the directionality is chosen randomly with even odds), or
2. one of the two division destinations is moved either clockwise or counter-clockwise (again with
50/50 odds).

Once a newly created cell has undergone mutation, it attempts to occupy its target destination. If
the destination is empty, then the division process ends for this cell. If, however, the location
is already occupied by another living cell, then the current occupant and the newly created cell
compete to survive. The competition is incredibly simple: the cell with the most energy wins and
occupies the cell, while the lower-energy cell is destroyed. Beyond this result, a game rule flag
decides what effect the conflict has on the winning cell's energy level:
- `costly_victory` results in the reduction of the winning cell's energy level by the loser's 
energy level, as if energy levels cancel out
- `standard_victory` results in the winner's energy level remaining unaffected
- `conquest_victory` results in the winner gaining energy equal to the loser's energy level, as if
the winner absorbes the loser

## Nitty Gritty Details
When counting neighbors, the count starts at 0 with the northern neighbor and proceeds clockwise.