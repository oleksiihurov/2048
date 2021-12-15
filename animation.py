# System imports
from enum import Enum, auto

# External imports
from numpy import sin, pi

# Project imports
from game import Tile
from config import GAME, TILE, ANIMATION


class PHASE(Enum):
    """Sequence of animation phases."""
    MOVING = auto()
    ARISING = auto()
    FINISH = auto()


# --- Animation ---------------------------------------------------------------

class Animation:

    def __init__(self):

        self.tiles: list[Tile] = list()
        self.phase = PHASE.MOVING

        # fpp - frames per phase.
        self.fpp_moving = int(ANIMATION.TIME_MOVING * ANIMATION.FPS)
        self.fpp_arising = int(ANIMATION.TIME_MOVING * ANIMATION.FPS)

        self.moving_coords = self.calculate_fpp_moving_coords()
        self.arising_scales = self.calculate_fpp_arising_scales()

    def calculate_fpp_moving_coords(self) -> dict[int, list[int]]:
        """
        Precalculating sequence of delta coords for all the distances,
        needed for moving phase of animation, using specific function.
        """

        def func(arg) -> float:
            """
            argument must be in a range: 0.0 <= arg <= 1.0
            return value in a range: 0.0 <= value <= 1.0
            """
            return sin(arg * pi / 2) ** 2

        result = dict()

        max_order = max(GAME.ROWS, GAME.COLS)
        for order in range(1, max_order):
            distance = order * (TILE.SIZE + TILE.PADDING)
            coords = [
                int(distance * func(delta / self.fpp_moving))
                for delta in range(self.fpp_moving)
            ]
            result[order] = coords

        return result

    def calculate_fpp_arising_scales(self) -> list[float]:
        """
        Precalculating sequence of scale multipliers,
        needed for arising phase of animation, using specific function.
        Note: fpp - frames per phase.
        """

        def func(arg) -> float:
            """
            argument must be in a range: 0.0 <= arg <= 1.0
            return value in a range: 0.0 <= value < 2.0
            """
            pass
            # https://www.desmos.com/calculator/yl60qp93x9

        result = [
            func(i / self.fpp_arising)
            for i in range(self.fpp_arising)
        ]

        return result

    def start(self, tiles: list[Tile]):

        # Step 1: interruption of any previous animation
        if self.phase is not PHASE.FINISH:
            pass

        # Step 2: starting new one
        self.tiles = tiles

        pass

    def next(self):

        # next slide of animation

        # next phase of animation

        pass
