#  Copyright (c) 2025.  Departamento de Ingenieria de Sistemas y Computacion
import logging
from dataclasses import dataclass
from typing import ClassVar, List, Optional
import numpy as np
from matplotlib import pyplot as plt
from tqdm import tqdm
from typeguard import typechecked
import seaborn as sns
import matplotlib
from scipy.signal import convolve2d
from benchmark import benchmark
from logger import configure_logging

matplotlib.use("TkAgg")

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
        """
        Expands the grid by adding a 1-cell border of DEAD cells around the current state.
        :return:
        """
        new_state = np.zeros(
            (self.state.shape[0] + 2, self.state.shape[1] + 2), dtype=int
        )
        new_state[1:-1, 1:-1] = self.state
        self.state = new_state

    # Trims any completely empty rows or columns from the edges of the grid.
    def reduce(self):
        """
        reduce the matrix by removing border rows and columns that contain only dead cells (zeros).
        """
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
    def count_neighbors(self) -> np.ndarray:
        """
        Count the number of alive neighbors for a given cell in the state.
        """
        # Define the kernel for counting neighbors
        # The kernel is a 3x3 matrix with 1s in all positions except the center
        # The center position is 0 because we don't want to count the cell itself
        kernel = np.array([
            [1, 1, 1],
            [1, 0, 1],
            [1, 1, 1],
        ])
        """
        convolve2d is a function from scipy that performs a 2D convolution
        a convolution is a mathematical operation that combines two functions
        in this case, we are combining the kernel with the state
        The result is a 2D array where each cell contains the number of alive neighbors
        """
        return convolve2d(self.state, kernel, mode="same", boundary="fill", fillvalue=0)

    # Evolves the game state to the next generation based on the rules of the game.
    def evolve(self):
        """
        Evolve the current state to the next generation.
        """
        self.expand()
        neighbors = self.count_neighbors()
        new_state = np.zeros_like(self.state)
        """
        np.logical_and is a function that returns the logical AND of two arrays
        and here is used to combine the conditions for the alive and dead cells
        """
        new_state[np.logical_and(self.state == self.ALIVE, np.logical_or(neighbors == 2, neighbors == 3))] = self.ALIVE
        new_state[np.logical_and(self.state == self.DEAD, neighbors == 3)] = self.ALIVE

        self.state = new_state
        self.reduce()
        self.generation += 1

    @typechecked
    def run_simulation(
        self,
        max_generations: Optional[int] = None,
        show_progress: Optional[bool] = False,
    ) -> str:
        """
        Run the simulation for a given number of generations.
        """
        if max_generations is None:
            max_generations = self.max_generations

        if max_generations <= 0:
            raise ValueError("max_generations must be positive")

        for _ in tqdm(
            range(0, max_generations),
            desc="Evolving generations",
            unit="gen",
            ncols=200,
            disable=not show_progress,
        ):
            # generate the next generation
            self.evolve()
            # if the population is 0, break the loop
            if self.population() == 0:
                return "WARN: Stopping simulation at:\n" + str(self)

        return str(self)

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
def plot_game_of_life(game_of_life: GameOfLife, path: Optional[str] = None) -> None:
    fig = plt.figure(facecolor="white", dpi=200)

    ax = plt.gca()
    ax.set_axis_off()

    sns.heatmap(
        game_of_life.state, #ndarray
        cmap="binary",
        cbar=False,
        square=True,
        linewidths=0.25,
        linecolor='#f0f0f0', # rgb
        ax=ax,
    )

    # Set the title
    plt.title("The Conway's Game of Life")

    # create some stats
    total_space = game_of_life.state.shape[0] * game_of_life.state.shape[1]
    density = game_of_life.population() / total_space
    stats=(
        f"Generation: {game_of_life.generation}\n",
        f"Population: {game_of_life.population()}\n",
        f"Max generations: {game_of_life.max_generations}\n",
        f"Grid size: {game_of_life.state.shape[0]} x {game_of_life.state.shape[1]}\n"
        f"Density: {density:.2f}\n"
    )
    # plot the stats
    plt.figtext(
        x=0.99,
        y=0.01,
        s="\n".join(stats),
        horizontalalignment="right",
        verticalalignment="bottom",
        fontsize=10,
        bbox=dict(facecolor="white", alpha=0.8, boxstyle="round", pad=0.5) #alpha is transparency
    )
    plt.tight_layout()

    if path is not None:
        plt.savefig(
            f"{path}/game_of_life-{game_of_life.generation:04d}.png",
            dpi=200,
            bbox_inches="tight",
        )

    plt.show()


def main():
    # configure the logger
    configure_logging()

    # hide some libraries
    logging.getLogger("matplotlib").setLevel(logging.WARNING)
    logging.getLogger("PIL").setLevel(logging.WARNING)

    # get the logger
    log = logging.getLogger(__name__)
    log.debug("Starting the Game of Life simulation")

    state = [
        [1, 1, 0],
        [0, 1, 1],
        [0, 1, 0],
    ]

    # The object Game Of Life
    game_of_life = GameOfLife.from_list(state)
    # Print the initial state
    print(f"The current live cells is {game_of_life.population()}")
    print(game_of_life)

    # run the simulation
    with benchmark(
        operation_name="run_simulation",
        log=log
    ):
        game_of_life.run_simulation(max_generations=1000, show_progress=True)

    # print the final state
    print(game_of_life)
    plot_game_of_life(game_of_life, path="../../output/")
    log.debug("The Game of Life simulation is over")

if __name__ == "__main__":
    main()
