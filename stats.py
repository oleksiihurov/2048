# -----------------------------------------------------------------------------
# "2048" tribute to original https://2048game.com
# Copyright (c) Dec 2021 Oleksii Hurov
# -----------------------------------------------------------------------------

"""
(I) Data level abstraction.
Data structures and interfaces.
"""


# Project imports
from config import MOVE


# --- Stats -------------------------------------------------------------------

class Stats:
    """Game statistics."""

    def __init__(self, rows: int, cols: int):
        self.score = 0
        self.score_incremental = 0
        self.move = {move: 0 for move in MOVE}
        self.moves_idle = 0
        self.merge = {i + 2: 0 for i in range(rows * cols + 1)}

    def reset(self, rows: int, cols: int):
        self.__init__(rows, cols)
