# System imports
from enum import Enum, auto

# External imports
import numpy as np


# --- Constants and Types -----------------------------------------------------

# maximum supported value for power of 2 value
# default value: 2 ** 32 = 4_294_967_295
MAX_POWER = 32

# appropriate numpy dtype for that value
# default value: np.uint32 = 4 bytes
MAX_POWER_TYPE = np.uint32


# supported moves: up, down, right, left
class MOVE(Enum):
    UP = auto()
    DOWN = auto()
    RIGHT = auto()
    LEFT = auto()


# --- Game classes ------------------------------------------------------------

class Stats:
    def __init__(self):
        self.score = 0
        self.score_incremental = 0
        self.move = {move: 0 for move in MOVE}
        self.moves_idle = 0
        self.merge = {4 << i: 0 for i in range(MAX_POWER - 1)}

    def erase(self):
        self.__init__()


class Game:

    def __init__(self, cols: int, rows: int):

        self.cols, self.rows = cols, rows
        #    x→          y,x
        #   ┌───┬───┬───┬───┐
        # y │0,0│0,1│0,2│   │
        # ↓ ├───┼───┼───┼───┤
        #   │1,0│1,1│   │   │
        #   ├───┼───┼───┼───┤
        #   │2,0│   │   │   │
        #   ├───┼───┼───┼───┤
        #   │   │   │   │3,3│
        #   └───┴───┴───┴───┘
        #       matrix[y][x]
        #   ┌───┬───┬───┬───┐
        #   │512│256│128│ 64│
        #   ├───┼───┼───┼───┤
        #   │ 4 │ 8 │ 16│ 32│
        #   ├───┼───┼───┼───┤
        #   │ 2 │   │   │   │
        #   ├───┼───┼───┼───┤
        #   │   │   │   │ 2 │
        #   └───┴───┴───┴───┘
        #    matrix = [[512, 256, 128, 64], [4, 8, 16, 32], [2, 0, 0, 0], [0, 0, 0, 2]]
        self.matrix = np.empty(
            shape=(self.rows, self.cols),
            dtype=MAX_POWER_TYPE
        )

        self.stats = Stats()

        self.init_matrix()
        # self.test_matrix()

    # --- Matrix initialization methods ---------------------------------------

    def clear_matrix(self):
        """
        Erase matrix by filling zeros.
        """
        self.matrix = np.zeros(
            shape=(self.rows, self.cols),
            dtype=MAX_POWER_TYPE
        )
        self.stats.erase()

    def init_matrix(self):
        """
        Initialize matrix with two new tiles in grid.
        """
        self.clear_matrix()
        self.generate_tile()
        self.generate_tile()

    def test_matrix(self):
        self.clear_matrix()
        max_power = self.rows * self.cols - 1
        test_list = [2 << i for i in range(max_power)]
        test_list = test_list[::-1]
        test_list = test_list + [0]
        self.matrix = np.array(test_list).reshape((self.rows, self.cols))

    def generate_tile(self, tile=2):
        """
        Generate new tile on a random empty place in the matrix.
        """
        if 0 in self.matrix:
            while True:
                x = np.random.randint(self.cols)
                y = np.random.randint(self.rows)
                if not self.matrix[y, x]:
                    self.matrix[y, x] = tile
                    break

    @staticmethod
    def choose_tile():
        """
        Return next generated tile
        with 90% probability of '2'
        and 10% probability of '4'.
        """
        return np.random.choice([2, 4], p=[0.9, 0.1])

    # --- Checking game state methods -----------------------------------------

    def is_game_lost(self):
        """
        Checking state of the game when it reaches no possible continuation.
        """

        # Step 1: Checking for any empty tile entries
        if 0 in self.matrix:
            return False

        # Step 2a: # Looking over horizontal paired tiles
        for y in range(self.rows):
            for x in range(self.cols - 1):
                if self.matrix[y, x] == self.matrix[y, x + 1]:
                    return False

        # Step 2b: # Looking over vertical paired tiles
        for x in range(self.cols):
            for y in range(self.rows - 1):
                if self.matrix[y, x] == self.matrix[y + 1, x]:
                    return False

        # Otherwise it's really lost game
        return True

    # --- Operations over matrix methods  -------------------------------------

    def reverse_matrix(self):
        """
        Flip the matrix horizontally.
        """
        #   ┌───┬───┬───┬───┐           ┌───┬───┬───┬───┐
        #   │ 0 │ 1 │ 2 │ 3 │           │ 3 │ 2 │ 1 │ 0 │
        #   ├───┼───┼───┼───┤           ├───┼───┼───┼───┤
        #   │ 4 │ 5 │ 6 │ 7 │ reverse → │ 7 │ 6 │ 5 │ 4 │
        #   ├───┼───┼───┼───┤           ├───┼───┼───┼───┤
        #   │ 8 │ 9 │ 10│ 11│           │ 11│ 10│ 9 │ 8 │
        #   └───┴───┴───┴───┘           └───┴───┴───┴───┘
        self.matrix = np.fliplr(self.matrix)

    def transpose_matrix(self):
        """
        Transpose the matrix.
        """
        #   ┌───┬───┬───┬───┐               ┌───┬───┬───┐
        #   │ 0 │ 1 │ 2 │ 3 │               │ 0 │ 4 │ 8 │
        #   ├───┼───┼───┼───┤               ├───┼───┼───┤
        #   │ 4 │ 5 │ 6 │ 7 │  transpose →  │ 1 │ 5 │ 9 │
        #   ├───┼───┼───┼───┤               ├───┼───┼───┤
        #   │ 8 │ 9 │ 10│ 11│               │ 2 │ 6 │ 10│
        #   └───┴───┴───┴───┘               ├───┼───┼───┤
        #                                   │ 3 │ 7 │ 11│
        #                                   └───┴───┴───┘
        self.matrix = np.transpose(self.matrix)

    def compress_tiles(self) -> bool:
        """
        Compress tiles to the left side.
        Return True/False as indication of any changes made.
        """
        #   ┌───┬───┬───┬───┬───┐               ┌───┬───┬───┬───┬───┐
        #   │128│ 64│ 32│ 64│   │               │128│ 64│ 32│ 64│   │
        #   ├───┼───┼───┼───┼───┤               ├───┼───┼───┼───┼───┤
        #   │   │ 16│ 8 │   │ 8 │               │ 16│ 8 │ 8 │   │   │
        #   ├───┼───┼───┼───┼───┤   compress →  ├───┼───┼───┼───┼───┤
        #   │   │ 4 │   │ 4 │ 2 │               │ 4 │ 4 │ 2 │   │   │
        #   ├───┼───┼───┼───┼───┤               ├───┼───┼───┼───┼───┤
        #   │ 2 │ 2 │ 2 │ 2 │ 2 │               │ 2 │ 2 │ 2 │ 2 │ 2 │
        #   └───┴───┴───┴───┴───┘               └───┴───┴───┴───┴───┘

        rows, cols = self.matrix.shape
        new = np.zeros_like(self.matrix)
        done = False

        for y in range(rows):
            x_new = 0
            for x in range(cols):
                if self.matrix[y, x]:
                    new[y, x_new] = self.matrix[y, x]
                    if x_new != x:
                        done = True
                    x_new += 1

        self.matrix = new
        return done

    def merge_tiles(self) -> bool:
        """
        Merge tiles to the left direction.
        Return True/False as indication of any changes made.
        """
        #   ┌───┬───┬───┬───┬───┐               ┌───┬───┬───┬───┬───┐
        #   │128│ 64│ 32│ 64│   │               │128│ 64│ 32│ 64│   │
        #   ├───┼───┼───┼───┼───┤               ├───┼───┼───┼───┼───┤
        #   │ 16│ 8 │ 8 │   │   │               │ 16│ 16│   │   │   │
        #   ├───┼───┼───┼───┼───┤   compress →  ├───┼───┼───┼───┼───┤
        #   │ 4 │ 4 │ 2 │   │   │               │ 8 │   │ 2 │   │   │
        #   ├───┼───┼───┼───┼───┤               ├───┼───┼───┼───┼───┤
        #   │ 2 │ 2 │ 2 │ 2 │ 2 │               │ 4 │   │ 4 │   │ 2 │
        #   └───┴───┴───┴───┴───┘               └───┴───┴───┴───┴───┘

        rows, cols = self.matrix.shape
        done = False

        for y in range(rows):
            for x in range(cols - 1):
                if self.matrix[y, x] and self.matrix[y, x] == self.matrix[y, x + 1]:
                    self.matrix[y, x] *= 2
                    self.matrix[y, x + 1] = 0

                    done = True
                    self.stats.score_incremental += self.matrix[y, x]
                    self.stats.merge[self.matrix[y, x]] += 1

        return done

    # --- Moves performed by player -------------------------------------------
    # The way to do tiles movement is compress → merge → compress again.
    # But before we have to orient matrix to universal position using reverse/transpose.
    # Reverse/transpose matrix operations should be performed in correct order.
    # After all matrix have to be transposed/reversed back to original orientation.

    def _move(self, move: MOVE) -> bool:
        """
        Internal wrapper for all four moves:
        up, down, right or left accordingly.
        Return True/False as indication of any changes made.
        """

        # Step 1: preparation to the move
        done1 = done2 = done3 = 0
        self.stats.score_incremental = 0

        # Step 2: orientation of the matrix before the move
        if move == MOVE.UP:
            self.transpose_matrix()
        elif move == MOVE.DOWN:
            self.transpose_matrix()
            self.reverse_matrix()
        elif move == MOVE.RIGHT:
            self.reverse_matrix()
        elif move == MOVE.LEFT:
            pass  # no matrix transformations

        # Step 3: the move itself
        done1 = self.compress_tiles()
        done2 = self.merge_tiles()
        if done2:
            done3 = self.compress_tiles()
        else:
            self.stats.moves_idle += 1

        # Step 4: orientation of the matrix back after the move
        if move == MOVE.UP:
            self.transpose_matrix()
        elif move == MOVE.DOWN:
            self.reverse_matrix()
            self.transpose_matrix()
        elif move == MOVE.RIGHT:
            self.reverse_matrix()
        elif move == MOVE.LEFT:
            pass  # no matrix transformations

        # Step 5: operations after the move
        done = done1 or done2 or done3
        self.stats.score += self.stats.score_incremental
        if done:
            self.stats.move[move] += 1

        return done

    def up(self) -> bool:
        """
        Shift tiles in the grid up.
        Return True/False as indication of any changes made.
        """
        return self._move(MOVE.UP)

    def down(self) -> bool:
        """
        Shift tiles in the grid down.
        Return True/False as indication of any changes made.
        """
        return self._move(MOVE.DOWN)

    def right(self) -> bool:
        """
        Shift tiles in the grid to the right.
        Return True/False as indication of any changes made.
        """
        return self._move(MOVE.RIGHT)

    def left(self) -> bool:
        """
        Shift tiles in the grid to the left.
        Return True/False as indication of any changes made.
        """
        return self._move(MOVE.LEFT)
