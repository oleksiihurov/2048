# -----------------------------------------------------------------------------
# "2048" tribute to original https://2048game.com
# Copyright (c) Dec 2021 Oleksii Hurov
# -----------------------------------------------------------------------------

"""
(III) Logic level abstraction.
Logic, primary purpose and calculations.
"""

# System imports
from collections import deque
from copy import copy

# External imports
import numpy as np

# Project imports
from config import MOVE
from stats import Stats
from tiles import Tiles

# --- Constants and Additional classes ----------------------------------------

# maximum supported value for power of 2 value
# default value: 2 ** 32 = 4_294_967_295
MAX_POWER = 32

# appropriate numpy dtype enough for a power of that value
# default value: np.uint16 = 2 bytes
MAX_POWER_TYPE = np.uint16


# --- Logic class --------------------------------------------------------------

class Logic:

    def __init__(self, game):

        # game matrix, which contains just base for power of '2'
        # but not the representative value itself
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
        #    matrix = [[9, 8, 7, 6], [2, 3, 4, 5], [1, 0, 0, 0], [0, 0, 0, 1]]
        self.cols = game.COLS
        self.rows = game.ROWS
        self.matrix = np.empty(
            shape = (self.rows, self.cols),
            dtype = MAX_POWER_TYPE
        )

        # game statistics
        self.stats = Stats(self.rows, self.cols)

        # game history for undo operation
        self.undo = game.UNDO
        self.history_matrix = deque(maxlen=self.undo) if self.undo else None
        self.history_stats = deque(maxlen=self.undo) if self.undo else None

        # tiles representation as objects for animation
        self.tiles = Tiles(self.rows, self.cols)

        self.new_game()
        # self.test_matrix()

    # --- Matrix initialization methods ---------------------------------------

    def test_matrix(self):
        """Matrix filled up by all tiles for testing purposes..."""
        self.clear_matrix()
        self.clear_stats()
        self.clear_history()
        max_power = self.rows * self.cols - 2
        test_list = [i + 1 for i in range(max_power)]
        test_list = [0] + [1] + test_list
        test_matrix = np.array(test_list).reshape((self.rows, self.cols))
        for y in range(1, test_matrix.shape[0], 2):
            test_matrix[y, :] = test_matrix[y, :][::-1]
        self.matrix = test_matrix
        self.tiles.copy_from_matrix(self.matrix)

    def clear_matrix(self):
        """Erase matrix by filling zeros."""
        self.matrix = np.zeros(
            shape = (self.rows, self.cols),
            dtype = MAX_POWER_TYPE
        )

    def clear_tiles(self):
        self.tiles.clear_tiles()

    def clear_stats(self):
        """Erasing game statistics."""
        self.stats.reset(self.rows, self.cols)

    def new_game(self):
        """Initialize matrix with two new tiles in grid."""
        self.clear_matrix()
        self.clear_tiles()
        self.clear_stats()
        self.clear_history()
        self.generate_new_tile()
        self.generate_new_tile()

    def generate_new_tile(self, value=None):
        """Generate new tile on a random empty place in the matrix."""
        if 0 in self.matrix:
            while True:
                row = np.random.randint(self.rows)
                col = np.random.randint(self.cols)
                if not self.matrix[row, col]:
                    if value is not None:
                        self.matrix[row, col] = value
                        self.tiles.arise_tile(row, col, value)
                    else:
                        self.matrix[row, col] = 1
                        self.tiles.new_tile(row, col, 1)
                    break

    @staticmethod
    def choose_tile():
        """
        Return next generated tile
        with 90% probability of '1'
        and 10% probability of '2'.
        """
        return np.random.choice([1, 2], p=[0.9, 0.1])

    # --- History methods -----------------------------------------------------

    def put_to_history(self, matrix, stats):
        """
        Saving to history of moves:
        current state of matrix and statistics.
        """
        if self.undo:
            self.history_matrix.append(matrix)
            self.history_stats.append(stats)

    def pop_from_history(self) -> bool:
        """
        Retrieving from history of moves:
        the most recent state of matrix and statistics.
        """
        if self.undo:
            if len(self.history_matrix):
                self.matrix = self.history_matrix.pop()
                self.tiles.copy_from_matrix(self.matrix)
                self.stats = self.history_stats.pop()
                return True
            else:
                return False

    def is_history_there(self) -> bool:
        """
        Checking if history stacks have any recently saved information.
        """
        if self.undo:
            return bool(len(self.history_matrix))
        else:
            return False

    def clear_history(self):
        """
        Erasing history stacks.
        """
        if self.undo:
            self.history_matrix.clear()
            self.history_stats.clear()

    # --- Checking game state methods -----------------------------------------

    def is_game_lost(self):
        """
        Checking state of the game when it reaches no possible continuation.
        """

        # Step 1: Checking for any empty tile entries
        if 0 in self.matrix:
            return False

        # Step 2a: # Looking over horizontal paired tiles
        for row in range(self.rows):
            for col in range(self.cols - 1):
                if self.matrix[row, col] == self.matrix[row, col + 1]:
                    return False

        # Step 2b: # Looking over vertical paired tiles
        for col in range(self.cols):
            for row in range(self.rows - 1):
                if self.matrix[row, col] == self.matrix[row + 1, col]:
                    return False

        # Otherwise it's really lost game
        return True

    def game_lost_procedure(self):
        from pprint import pprint
        print('Game lost!\n')
        print(self.matrix)
        print(f'\n{self.stats.score = }')
        print(f'\n{self.stats.moves_idle = }')
        print(f'\nTotal moves = {sum(self.stats.move.values())}')
        print()
        [print(f'{k} = {v}') for k, v in self.stats.move.items()]
        print()
        pprint({k: v for k, v in self.stats.merge.items() if v})
        # TODO rework

    # --- Operations over matrix methods  -------------------------------------

    def flip_matrix(self):
        """
        Flip the matrix horizontally.
        """
        #   ┌───┬───┬───┬───┐          ┌───┬───┬───┬───┐
        #   │ 0 │ 1 │ 2 │ 3 │          │ 3 │ 2 │ 1 │ 0 │
        #   ├───┼───┼───┼───┤          ├───┼───┼───┼───┤
        #   │ 4 │ 5 │ 6 │ 7 │ fliplr → │ 7 │ 6 │ 5 │ 4 │
        #   ├───┼───┼───┼───┤          ├───┼───┼───┼───┤
        #   │ 8 │ 9 │ 10│ 11│          │ 11│ 10│ 9 │ 8 │
        #   └───┴───┴───┴───┘          └───┴───┴───┴───┘
        self.matrix = np.fliplr(self.matrix)
        self.tiles.fliplr()

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
        self.tiles.transpose()

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
        matrix_new = np.zeros_like(self.matrix)
        done = False

        for row in range(rows):
            col_new = 0
            for col in range(cols):
                if self.matrix[row, col]:
                    matrix_new[row, col_new] = self.matrix[row, col]
                    if col_new != col:
                        self.tiles.move_tile(row, col, row, col_new)
                        done = True
                    col_new += 1

        self.matrix = matrix_new
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

        for row in range(rows):
            for col in range(cols - 1):
                if self.matrix[row, col] and \
                        self.matrix[row, col] == self.matrix[row, col + 1]:
                    self.matrix[row, col] += 1
                    self.matrix[row, col + 1] = 0
                    self.tiles.move_tile(row, col + 1, row, col)
                    self.tiles.arise_tile(row, col, int(self.matrix[row, col]))
                    done = True

                    self.stats.score_incremental += 2 ** int(self.matrix[row, col])
                    self.stats.merge[self.matrix[row, col]] += 1

        return done

    # --- Moves performed by player -------------------------------------------
    # The way to do tiles movement is compress → merge → compress again.
    # But before we have to orient matrix to universal position using flip/transpose.
    # Reverse/transpose matrix operations should be performed in correct order.
    # After all matrix have to be transposed/flipped back to original orientation.

    def up(self) -> MOVE:
        """
        Shift tiles in the grid up.
        Return type of MOVE as indication of any changes made.
        """
        return self._move(MOVE.UP)

    def down(self) -> MOVE:
        """
        Shift tiles in the grid down.
        Return type of MOVE as indication of any changes made.
        """
        return self._move(MOVE.DOWN)

    def right(self) -> MOVE:
        """
        Shift tiles in the grid to the right.
        Return type of MOVE as indication of any changes made.
        """
        return self._move(MOVE.RIGHT)

    def left(self) -> MOVE:
        """
        Shift tiles in the grid to the left.
        Return type of MOVE as indication of any changes made.
        """
        return self._move(MOVE.LEFT)

    def _move(self, move: MOVE) -> MOVE:
        """
        Internal wrapper for all four moves:
        up, down, right or left accordingly.
        Return type of MOVE as indication of any changes made.
        """

        # Step 1: preparation to the move
        backup_matrix = copy(self.matrix)
        backup_stats = copy(self.stats)
        self.tiles.copy_from_matrix(self.matrix)
        self.tiles.set_move(move)
        done1 = done2 = done3 = 0
        self.stats.score_incremental = 0

        # Step 2: orientation of the matrix before the move
        if move == MOVE.UP:
            self.transpose_matrix()
        elif move == MOVE.DOWN:
            self.transpose_matrix()
            self.flip_matrix()
        elif move == MOVE.RIGHT:
            self.flip_matrix()
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
            self.flip_matrix()
            self.transpose_matrix()
        elif move == MOVE.RIGHT:
            self.flip_matrix()
        elif move == MOVE.LEFT:
            pass  # no matrix transformations

        # Step 5: operations after the move
        done = done1 or done2 or done3
        self.stats.score += self.stats.score_incremental
        if done:
            self.stats.move[move] += 1
            self.put_to_history(backup_matrix, backup_stats)
            result = move
        else:
            result = MOVE.NONE

        return result
