# External imports
from numpy import sin, pi

# Project imports
from config import GAME, TILE, GRID, ANIMATION, MOVE, PHASE


# --- Tile --------------------------------------------------------------------

class Tile:
    """Tile object for animation."""

    def __init__(
            self,
            row_from: int, col_from: int,
            value: int,
            moving = False,
            arising = False
    ):
        """
        Tile object for animation.

        :param value: value from the appropriate self.matrix[row, col] cell
        :param row_from: starting row in the grid for the tile
        :param col_from: starting column in the grid for the tile
        :param moving: flag: is this tile going to move or not?
        :param arising: flag: is it newly appeared tile or not?
        """

        # starting row & column in the grid for the tile
        self.row_from, self.col_from = row_from, col_from
        # destination row & column in the grid for the moving tile
        self.row_to, self.col_to = row_from, col_from

        # corresponding value as base for power of '2'
        self.value = value

        # marking corresponding animation phases
        self.moving = moving
        self.arising = arising

        # number of rows or columns needed to move during animation
        self.distance = 0

        # graphics coords [x, y] of the tile related to GRID position
        # change during moving animation phase
        self.x_from = self.y_from = 0
        self.x = self.y = 0
        self.x_to = self.y_to = 0

        # graphics resize multiplier of the tile surface on the GRID
        # changes during arising animation phase
        self.scale = 1

        # flag for showing tile
        self.show = True


# --- Tiles -------------------------------------------------------------------

class Tiles:
    """Alternative way of representing matrix of tiles, using tile objects."""

    def __init__(self, rows: int, cols: int):

        # defining the "matrix" of tiles
        self.rows, self.cols = rows, cols
        self.tiles: list[Tile] = list()

        # defining current state of animation
        self.move = MOVE.NONE
        self.phase = PHASE.MOVING
        self.frame = 0

        # fpp - frames per phase.
        self.fpp_moving = int(ANIMATION.TIME_MOVING * ANIMATION.FPS)
        self.fpp_arising = int(ANIMATION.TIME_ARISING * ANIMATION.FPS)

        # lists of corresponding changes in animated frames
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

    def _find_index(self, row: int, col: int) -> int:
        index = None
        for i, tile in enumerate(self.tiles):
            if tile.row_from == row and tile.col_from == col:
                index = i
                break
        return index

    def get_tile(self, row: int, col: int) -> Tile:
        return self.tiles[self._find_index(row, col)]

    def set_tile(self, row: int, col: int, tile: Tile):
        self.tiles[self._find_index(row, col)] = tile

    def get_value(self, row: int, col: int) -> int:
        return self.tiles[self._find_index(row, col)].value

    def set_value(self, row: int, col: int, value: int):
        self.tiles[self._find_index(row, col)].value = value

    def copy_from_matrix(self, matrix):
        for row in range(self.rows):
            for col in range(self.cols):
                if matrix[row, col]:
                    self.tiles.append(Tile(row, col, matrix[row, col]))

    def arise_tile(self, row: int, col: int, value: int):
        self.tiles.append(Tile(row, col, value, arising=True))

    def move_tile(self, row_from: int, col_from: int, row_to: int, col_to: int):
        with self.tiles[self._find_index(row_from, col_from)] as tile:
            tile.row_to = row_to
            tile.col_to = col_to
            tile.moving = True

    def reverse(self):
        for tile in self.tiles:
            tile.col_from = (self.cols - 1) - tile.col_from
            tile.col_to = (self.cols - 1) - tile.col_to

    def transpose(self):
        for tile in self.tiles:
            tile.row_from, tile.col_from = tile.col_from, tile.row_from
            tile.row_to, tile.col_to = tile.col_to, tile.row_to

    # --- Animation methods ---------------------------------------------------

    def start_animation(self, move: MOVE):
        """Starting new animation procedure."""

        # Step 1: interruption of any previous animation
        self.phase = PHASE.MOVING
        self.frame = 0

        # Step 2: starting new animation
        self.move = move

        # preparation of all the graphics attributes for tiles
        for tile in self.tiles:

            # during moving phase we do show arising tiles
            if tile.arising:
                tile.show = False

            # calculating distances for moving tiles
            if tile.moving:
                if self.move == MOVE.UP:
                    tile.distance = tile.row_from - tile.row_to
                elif self.move == MOVE.DOWN:
                    tile.distance = tile.row_to - tile.row_from
                elif self.move == MOVE.RIGHT:
                    tile.distance = tile.col_to - tile.col_from
                elif self.move == MOVE.LEFT:
                    tile.distance = tile.col_from - tile.col_to
                else:
                    raise ValueError(f"Unexpected move value: {self.move}")

            # calculating coords [x, y] for all tiles
            tile.x_from = \
                GRID.X_TOP_LEFT + TILE.PADDING + TILE.SIZE // 2 + \
                tile.col_from * (TILE.SIZE + TILE.PADDING)
            tile.y_from = \
                GRID.Y_TOP_LEFT + TILE.PADDING + TILE.SIZE // 2 + \
                tile.row_from * (TILE.SIZE + TILE.PADDING)

            tile.x = tile.x_from
            tile.y = tile.y_from

            tile.x_to = \
                GRID.X_TOP_LEFT + TILE.PADDING + TILE.SIZE // 2 + \
                tile.col_to * (TILE.SIZE + TILE.PADDING)
            tile.y_to = \
                GRID.Y_TOP_LEFT + TILE.PADDING + TILE.SIZE // 2 + \
                tile.row_to * (TILE.SIZE + TILE.PADDING)

        self.next_animation()

    def next_animation(self):
        """Performing the next animation slide."""
        pass

    def finish_moving(self):
        pass

    def finish_arising(self):
        pass
