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
    max_generations: int = 1000

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


if __name__ == "__main__":
    main()
