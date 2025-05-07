#  Copyright (c) 2025.  Departamento de Ingenieria de Sistemas y Computacion

from dataclasses import dataclass
from typing import ClassVar, List
import numpy as np
from matplotlib import pyplot as plt
from tqdm import tqdm
from typeguard import typechecked
import seaborn as sns

@typechecked
@dataclass
class GameOfLife:
    """
    Conway's Game of Life implementation.
    A Python implementation of Conway's Game of Life, a cellular automaton
    devised by John Conway in 1970.

    The game of life consist of a 2D grid of cells, each of which can be either
    alive or dead. There's a simple set of rules that determine the next state
    of the grid based on the current state. The rules are as follows:
    1. Any live cell with fewer than two live neighbors dies as if caused by
    under-population.
    2. Any live cell with two or three live neighbors lives on to the next
    generation.
    3. Any live cell with more than three live neighbors dies, as if by
    over-population.
    4. Any dead cell with exactly three live neighbors becomes a live cell,
    as if by reproduction.

    The game is played in generations, where each generation is a new state
    of the grid.
    The game ends when there are no live cells left or when the grid reaches a
    stable state.
    The class provides methods to evolve the game, print the current state,
    and count the population.
    The class also provides a method to create a new game from a list of lists.
    The class uses NumPy for efficient array manipulation and type checking.
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
    def from_list(cls, initial_state: List[List[int]]) -> "GameOfLife":
        # TODO: (eortiz) validate the initial state

        return cls(state=np.array(initial_state))

    # Returns the number of currently alive cells.
    def population(self) -> np.int64:
        # Sum the ALIVE cells
        return np.sum(self.state)

    # Prints the current grid state using live/dead cell characters.
    def print_state(self):
        for row in self.state:
            print(
                "".join(
                    self.live_cell_char if cell == self.ALIVE else self.dead_cell_char
                    for cell in row
                )
            )

    # Adds a 1-cell border of DEAD cells around the current state to allow growth.
    def expand(self):
        new_state = np.zeros(
            (self.state.shape[0] + 2, self.state.shape[1] + 2), dtype=int
        )
        new_state[1:-1, 1:-1] = self.state
        self.state = new_state

    # Trims any completely empty rows or columns from the edges of the grid.
    def reduce(self):
        row, col = self.state.shape

        def empty_row(r):
            return np.all(self.state[r, :] == self.DEAD)

        def empty_col(c):
            return np.all(self.state[:, c] == self.DEAD)

        top = 0
        while top < row and empty_row(top):
            top += 1

        bottom = row - 1
        while bottom >= 0 and empty_row(bottom):
            bottom -= 1

        left = 0
        right = col - 1
        while left < col and empty_col(left):
            left += 1
        while right >= 0 and empty_col(right):
            right -= 1

        if top > bottom or left > right:
            print(f"The simulation is over, the cell population is {self.population()}")
            self.state = np.array([0])
        else:
            self.state = self.state[top : bottom + 1, left : right + 1]

    # Returns the number of ALIVE neighbors around a given cell.
    def count_neighbors(self, row: int, col: int) -> int:
        neighbors = 0
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if (
                    r == row
                    and c == col
                    or r < 0
                    or c < 0
                    or r >= self.state.shape[0]
                    or c >= self.state.shape[1]
                ):
                    continue
                if self.state[r][c] == self.ALIVE:
                    neighbors += 1
        return neighbors

    # Evolves the game state to the next generation based on the rules of the game.
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

    def __str__(self):
        """Return a string representation of the current state"""
        return "\n".join(
            "".join(
                self.live_cell_char if cell == self.ALIVE else self.dead_cell_char
                for cell in row
            )
        for row in self.state
        )

@typechecked
def plot_game_of_life(game_of_life: GameOfLife) -> None:
    fig = plt.figure(figsize=(10, 10), facecolor="white")

    ax = plt.gca()
    sns.heatmap(
        game_of_life.state, #ndarray
        cmap="binary",
        square=True,
        linewidths=0.25,
        linecolor="grey",
        ax=ax,
    )

    plt.tight_layout()
    plt.show()

def main():
    state = [
        [1, 1, 0],
        [0, 1, 1],
        [0, 1, 0],
    ]

    # The object Game Of Life
    game_of_life = GameOfLife.from_list(state)
    # Print the initial state
    print(f"The current live cells is {game_of_life.population()}")
    #game_of_life.print_state()
    print(game_of_life)

    # Evolve the game for a number of generations
    for _ in tqdm(
            range(game_of_life.max_generations), desc="Evolving the Game of Life", unit="gen", ncols=80
    ):
        game_of_life.evolve()
        print(
            f"Generation {game_of_life.generation}, population {game_of_life.population()}"
        )
        #game_of_life.print_state()
        # Now thanks to __str__ method we can print the matrix
        #print(game_of_life)
        plot_game_of_life(game_of_life)


if __name__ == "__main__":
    main()
