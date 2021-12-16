# System imports
from enum import Enum, auto

# External imports
from numpy import sin, pi

# Project imports
from game import MOVE, Tile
from config import GAME, TILE, GRID, ANIMATION


class PHASE(Enum):
    """Sequence of animation phases."""
    MOVING = auto()
    ARISING = auto()
    FINISH = auto()


# --- Animation ---------------------------------------------------------------

class Animation:
    """Class of animation procedures for graphics."""

    def __init__(self):

        self.tiles: list[Tile] = list()
        self.move = MOVE.NONE
        self.phase = PHASE.MOVING
        self.frame = 0

        # fpp - frames per phase.
        self.fpp_moving = int(ANIMATION.TIME_MOVING * ANIMATION.FPS)
        self.fpp_arising = int(ANIMATION.TIME_MOVING * ANIMATION.FPS)

        self.moving_coords = self.calculate_fpp_moving_coords()
        self.arising_scales = self.calculate_fpp_arising_scales()

    # --- Pre-calculation methods ---------------------------------------------

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

        max_distance = max(GAME.ROWS, GAME.COLS)
        for distance in range(1, max_distance):
            length = distance * (TILE.SIZE + TILE.PADDING)
            coords = [
                int(length * func(delta / self.fpp_moving))
                for delta in range(self.fpp_moving)
            ]
            result[distance] = coords

        return result

    def calculate_fpp_arising_scales(self) -> list[float]:
        """
        Precalculating sequence of scale multipliers,
        needed for arising phase of animation, using specific function.
        """

        def func(arg) -> float:
            # TODO remake: (1) start not from 0 (2) sequence of sine functions
            """
            argument must be in a range: 0.0 <= arg <= 1.0
            return value in a range: 0.0 <= value <~ 1.2
            """
            a = 0.8
            b = (TILE.SIZE + TILE.PADDING) / TILE.SIZE
            if arg <= a:
                return arg * b / a
            else:
                return 2 * b - arg * b / a

        result = [
            func(i / self.fpp_arising)
            for i in range(self.fpp_arising)
        ]

        return result

    # --- Operational methods -------------------------------------------------

    def reset(self):
        """Erasing everything for new animation."""

        self.tiles.clear()
        self.phase = PHASE.MOVING
        self.frame = 0

    def start(self, tiles: list[Tile], move: MOVE):
        """Starting new animation procedure."""

        # Step 1: interruption of any previous animation
        if self.phase is not PHASE.FINISH:
            self.reset()

        # Step 2: starting new animation
        self.tiles = tiles
        self.move = move

        for tile in self.tiles:

            # calculating coords [x, y] for all tiles
            tile.x = tile.x_from = \
                GRID.X_TOP_LEFT + TILE.PADDING + TILE.SIZE // 2 + \
                tile.col_from * (TILE.SIZE + TILE.PADDING)
            tile.y = tile.y_from = \
                GRID.Y_TOP_LEFT + TILE.PADDING + TILE.SIZE // 2 + \
                tile.row_from * (TILE.SIZE + TILE.PADDING)

            # filling up distance for moving tiles
            if tile.moving:
                if tile.row_to is not None:
                    tile.distance = abs(tile.row_to - tile.row_from)
                else:  # tile.col_to is not None
                    tile.distance = abs(tile.col_to - tile.col_from)

        self.next()

    def next(self):
        """Performing the following animation step."""

        if self.phase == PHASE.FINISH:
            return

        if self.phase == PHASE.MOVING:

            for tile in self.tiles:
                if tile.moving:
                    if self.move == MOVE.UP:
                        tile.y = tile.y_from - \
                                 self.moving_coords[tile.distance][self.frame]
                    elif self.move == MOVE.DOWN:
                        tile.y = tile.y_from + \
                                 self.moving_coords[tile.distance][self.frame]
                    elif self.move == MOVE.RIGHT:
                        tile.x = tile.x_from + \
                                 self.moving_coords[tile.distance][self.frame]
                    elif self.move == MOVE.LEFT:
                        tile.x = tile.x_from - \
                                 self.moving_coords[tile.distance][self.frame]

        # next slide of animation

        # next phase of animation

        # case when no arising tiles exist at all

        self.frame += 1

        # Step 3: checking switch to the next phase
        if self.phase == PHASE.MOVING:
            if self.frame == self.fpp_moving:
                self.phase = PHASE.ARISING
        if self.phase == PHASE.ARISING:
            if self.frame == self.fpp_arising:
                self.phase = PHASE.FINISH
                self.finish()

    def finish(self):
        """Setting all the tiles to their final static positions."""
        pass
