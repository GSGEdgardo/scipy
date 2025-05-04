#  Copyright (c) 2025.  Departamento de Ingenieria de Sistemas y Computacion

from dataclasses import dataclass
from typing import ClassVar, List
import numpy as np
from typeguard import typechecked


@typechecked
@dataclass
class GameOfLife:
    """
    Conway's Game of Life implementation.
    TODO: (eortiz) write full documentation.
    """

    # The state of the Game of Life (2D grid)
    state: np.ndarray

    # Current generation number
    generation: int = 0

    # Maximum number of generations allowed
    max_generations: int = 151

    # Character used to represent a dead cell
    dead_cell_char: str = " "

    # Character used to represent a live cell
    live_cell_char: str = "࿕"

    # Class-level constants to represent cell states
    ALIVE: ClassVar[int] = 1
    DEAD: ClassVar[int] = 0

    # Validation logic after object creation
    def __post_init__(self) -> None:
        # State must be a NumPy array
        if not isinstance(self.state, np.ndarray):
            raise TypeError("Game of Life state must be a numpy array")

        # State must be a 2D matrix
        if self.state.ndim != 2:
            raise TypeError("Game of Life state must be a 2D array")

        # State must contain only 0 (DEAD) or 1 (ALIVE)
        if not np.all(np.isin(self.state, [self.ALIVE, self.DEAD])):
            raise TypeError("Game of Life state must contain only cells 0 and 1")

        # max_generations must be a positive integer
        if self.max_generations <= 0:
            raise TypeError("max_generations must be greater than 0")

    @classmethod
    @typechecked
    def from_list(cls, initial_state: List[List[int]]) -> 'GameOfLife':
        # TODO: (eortiz) validate the initial state

        return cls(state=np.array(initial_state))

    def population(self) -> np.int64:
        # Sum the ALIVE cells
        return np.sum(self.state)

    def print_state(self):
        for row in self.state:
            print(
                "".join(
                    self.live_cell_char
                    if cell == self.ALIVE
                    else self.dead_cell_char
                    for cell in row
                )
            )

    def expand(self):
        # Creates a new state with an extra row and column at the beginning and end
        new_state = np.zeros((self.state.shape[0] + 2, self.state.shape[1] + 2), dtype=int)
        # Fill the new state with the current state
        new_state[1:-1, 1:-1] = self.state
        self.state = new_state

    def reduce(self):
        row, col = self.state.shape

        def empty_row(r):
            return np.all(self.state[r,:] == self.DEAD)
        def empty_col(c):
            return np.all(self.state[:, c] == self.DEAD)

        top = 0
        while top < row and empty_row(top): top += 1

        bottom = row - 1
        while bottom >= 0 and empty_row(bottom): bottom -= 1

        left = 0
        right = col - 1
        while left < col and empty_col(left): left += 1
        while right >= 0 and empty_col(right): right -= 1

        if top > bottom or left > right:
            print(f"The simulation is over, the cell population is {self.population()}")
            self.state = np.array([0])
        else:
            self.state = self.state[top:bottom+1, left:right+1]

    def count_neighbors(self, row: int, col: int) -> int:
        neighbors = 0
        for r in range(row-1, row+2):
            for c in range(col-1, col+2):
                if (r == row and c == col or
                    r < 0 or c < 0 or
                    r >= self.state.shape[0] or
                    c >= self.state.shape[1]):
                    continue
                if self.state[r][c] == self.ALIVE:
                    neighbors += 1
        return neighbors

    def evolve(self):
        self.expand()
        new_state = np.zeros_like(self.state)
        row, col = self.state.shape

        for r in range(row):
            for c in range(col):
                neighbors = self.count_neighbors(r, c)
                if self.state[r][c] == self.ALIVE:
                    if neighbors < 2 or neighbors > 3:
                        new_state[r][c] = self.DEAD
                    else:
                        new_state[r][c] = self.ALIVE
                else:
                    if neighbors == 3:
                        new_state[r][c] = self.ALIVE
                    else:
                        new_state[r][c] = self.DEAD
        self.state = new_state
        self.reduce()
        self.generation += 1

def main():
    state = [
        [1, 1, 0],
        [0, 1, 1],
        [0, 1, 0],
    ]

    # The object Game Of Life
    game_of_life = GameOfLife.from_list(state)
    print(f"The current live cells is {game_of_life.population()}")
    game_of_life.print_state()

    for _ in range(game_of_life.max_generations):
        game_of_life.evolve()
        print(f"Generation {game_of_life.generation}, population {game_of_life.population()}")
        game_of_life.print_state()


if __name__ == "__main__":
    main()
