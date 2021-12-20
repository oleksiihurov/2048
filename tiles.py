# External imports
from numpy import sin, pi

# Project imports
from config import GAME, TILE, GRID, ANIMATION, MOVE, PHASE


# --- Tile --------------------------------------------------------------------

class Tile:
    """Tile object for animation."""

    def __init__(
            self,
            row: int, col: int,
            value: int,
            moving = False,
            arising = False
    ):
        """
        Tile object for animation.

        :param value: value from the appropriate self.matrix[row, col] cell
        :param row: starting row in the grid for the tile
        :param col: starting column in the grid for the tile
        :param moving: flag: is this tile going to move or not?
        :param arising: flag: is it newly appeared tile or not?
        """

        # starting cell in the grid for the tile
        self.row, self.col = row, col
        # destination cell in the grid for the moving tile
        self.row_to, self.col_to = row, col

        # corresponding value as base for power of '2'
        self.value = value

        # marking corresponding animation phases
        self.moving = moving
        self.arising = arising

        # number of rows or columns needed to move during moving phase
        self.distance = 0

        # graphics coords [x, y] of the tile related to GRID position
        # change during moving animation phase
        self.x = self.x_from = 0
        self.y = self.y_from = 0

        # graphics resize multiplier of the tile surface on the GRID
        # changes during arising animation phase
        self.scale = 1

        # visibility flag for tile
        self.show = not arising


# --- Tiles -------------------------------------------------------------------

class Tiles:
    """Alternative way of representing grid of tiles, using tile objects."""

    def __init__(self, rows: int, cols: int):

        # defining the "matrix" of tiles
        self.rows, self.cols = rows, cols
        self.tiles: list[Tile] = list()

        # defining current state of animation
        self.move = MOVE.NONE
        self.phase = PHASE.FINISH
        self.frame = 0

        # fpp - frames per phase.
        self.fpp_moving = int(ANIMATION.TIME_MOVING * ANIMATION.FPS)
        self.fpp_arising = int(ANIMATION.TIME_ARISING * ANIMATION.FPS)

        # lists of corresponding changes in animated frames
        self.moving_coords = self._precalculate_fpp_moving_coords()
        self.arising_scales = self._precalculate_fpp_arising_scales()

    # --- Pre-calculation methods ---------------------------------------------

    @staticmethod
    def _precalculate_function(arg: float, a = 0.0) -> float:
        """
        :param arg: must be in a range: 0.0 <= arg <= 1.0
        :param a: must be in a range: 0.0 <= a <= 1.0
        :return: value in a range: a <= return <= 1.0
        """
        return a + (1 - a) * sin(arg * pi / 2) ** 2

    def _precalculate_fpp_moving_coords(self) -> dict[int, list[int]]:
        """
        Precalculating sequence of delta coords for all the distances,
        needed for moving phase of animation, using specific function.
        """

        result = dict()

        max_distance = max(GAME.ROWS, GAME.COLS)
        for distance in range(1, max_distance):
            length = distance * (TILE.SIZE + TILE.PADDING)
            coords = [
                int(length * self._precalculate_function(i / self.fpp_moving))
                for i in range(self.fpp_moving)
            ]
            result[distance] = coords

        return result

    def _precalculate_fpp_arising_scales(self) -> list[float]:
        """
        Precalculating sequence of scale multipliers,
        needed for arising phase of animation, using specific function.
        """

        scales = [
            self._precalculate_function(i / self.fpp_arising, 0.5)
            for i in range(self.fpp_arising)
        ]

        return scales

    # --- Operational methods -------------------------------------------------

    # def _find_index(self, row: int, col: int) -> int:
    #     # first we search in the destination ('_to') tile-attributes
    #     for index, tile in enumerate(self.tiles):
    #         if tile.row_to == row and tile.col_to == col:
    #             return index
    #     # second we search in the current tile-attributes
    #     for index, tile in enumerate(self.tiles):
    #         if tile.row == row and tile.col == col:
    #             return index
    #     # otherwise it's an exception
    #     raise LookupError(f"Can't find any tile on position: {row=}, {col=}")

    def _find_indexes(self, row: int, col: int) -> list[int]:
        result = []
        # first we search in the destination ('_to') tile-attributes
        for index, tile in enumerate(self.tiles):
            if tile.row_to == row and tile.col_to == col:
                result.append(index)
        if not result:
            # second we search in the current tile-attributes
            for index, tile in enumerate(self.tiles):
                if tile.row == row and tile.col == col:
                    result.append(index)
        if not result:
            # if we didn't found anything - it's an exception
            raise LookupError(f"Can't find any tile on position: {row=}, {col=}")
        return result

    # def get_tile(self, row: int, col: int) -> Tile:
    #     return self.tiles[self._find_index(row, col)]
    #
    # def set_tile(self, row: int, col: int, tile: Tile):
    #     self.tiles[self._find_index(row, col)] = tile
    #
    # def get_value(self, row: int, col: int) -> int:
    #     return self.tiles[self._find_index(row, col)].value
    #
    # def set_value(self, row: int, col: int, value: int):
    #     self.tiles[self._find_index(row, col)].value = value

    def clear_tiles(self):
        self.tiles.clear()

    def new_tile(self, row: int, col: int, value: int):
        self.tiles.append(Tile(row, col, value))
        self._actualize_coords(len(self.tiles) - 1)

    def arise_tile(self, row: int, col: int, value: int):
        self.tiles.append(Tile(row, col, value, arising=True))

    def move_tile(self, row: int, col: int, row_to: int, col_to: int):
        indexes = self._find_indexes(row, col)
        for index in indexes:
            self.tiles[index].row_to = row_to
            self.tiles[index].col_to = col_to
            self.tiles[index].moving = True

    def copy_from_matrix(self, matrix):
        self.clear_tiles()
        for row in range(self.rows):
            for col in range(self.cols):
                if matrix[row, col]:
                    self.new_tile(row, col, int(matrix[row, col]))

    def set_move(self, move: MOVE):
        self.move = move

    def fliplr(self):
        for tile in self.tiles:
            tile.col = (self.cols - 1) - tile.col
            tile.col_to = (self.cols - 1) - tile.col_to

    def transpose(self):
        self.rows, self.cols = self.cols, self.rows
        for tile in self.tiles:
            tile.row, tile.col = tile.col, tile.row
            tile.row_to, tile.col_to = tile.col_to, tile.row_to

    # --- Animation methods ---------------------------------------------------

    def _reset_phase(self):
        self.phase = PHASE.MOVING
        self.frame = 0

    def _next_phase(self):
        if self.phase == PHASE.MOVING:
            self.phase = PHASE.ARISING
        elif self.phase == PHASE.ARISING:
            self.phase = PHASE.FINISH
        self.frame = 0

    def _actualize_coords(self, index: int):
        """
        Calculating coords [x, y] for the tile by index
        according to it's row & column.
        """
        self.tiles[index].x = self.tiles[index].x_from = \
            GRID.X_TOP_LEFT + TILE.PADDING + TILE.SIZE // 2 + \
            self.tiles[index].col * (TILE.SIZE + TILE.PADDING)
        self.tiles[index].y = self.tiles[index].y_from = \
            GRID.Y_TOP_LEFT + TILE.PADDING + TILE.SIZE // 2 + \
            self.tiles[index].row * (TILE.SIZE + TILE.PADDING)

    def _finish_moving(self):
        """
        Finalizing state of tiles
        to static picture after moving phase.
        """

        for index, tile in enumerate(self.tiles):

            if tile.moving:
                # actualizing cells in the grid for the tile
                tile.row = tile.row_to
                tile.col = tile.col_to
                tile.distance = 0

                self._actualize_coords(index)

                # disabling moving flag once it is done
                tile.moving = False

            # restoring visibility for arising tiles
            if tile.arising:
                tile.show = True
                tile.scale = 0

        # looking for overlapping tiles,
        # which always should be under arising tiles
        overlapping_cells: list[tuple[int, int]] = []
        for tile in self.tiles:
            if tile.arising:
                overlapping_cells.append((tile.row, tile.col))

        # retrieving indexes of overlapping tiles to delete
        overlapping_indexes: list[int] = []
        for index, tile in enumerate(self.tiles):
            if not tile.arising:
                if (tile.row, tile.col) in overlapping_cells:
                    overlapping_indexes.append(index)
        overlapping_indexes.reverse()

        # deleting overlapping tiles by indexes
        if overlapping_indexes:
            for index in overlapping_indexes:
                self.tiles.pop(index)

    def _finish_arising(self):
        """
        Finalizing state of tiles
        to static picture after arising phase.
        """

        # Step 2: finalizing other attributes
        for tile in self.tiles:
            if tile.arising:
                tile.scale = 1
                # disabling arising flag once it is done
                tile.arising = False

    def start_animation(self):
        """Starting new animation procedure."""

        self._reset_phase()

        for index, tile in enumerate(self.tiles):

            # calculating distances for moving tiles
            if tile.moving:
                if self.move == MOVE.UP:
                    tile.distance = tile.row - tile.row_to
                elif self.move == MOVE.DOWN:
                    tile.distance = tile.row_to - tile.row
                elif self.move == MOVE.RIGHT:
                    tile.distance = tile.col_to - tile.col
                elif self.move == MOVE.LEFT:
                    tile.distance = tile.col - tile.col_to
                else:
                    raise ValueError(f"Unexpected move value: {self.move}")

            self._actualize_coords(index)

        self.next_animation()

    def next_animation(self):
        """Performing the next animation slide."""

        # Step 1: skipping if animation was already finished
        if self.phase == PHASE.FINISH:
            return

        # Step 2: moving phase of animation
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
                    else:
                        raise ValueError(f"Unexpected move value: {self.move}")

        # Step 3: arising phase of animation
        if self.phase == PHASE.ARISING:
            for tile in self.tiles:
                if tile.arising:
                    tile.scale = self.arising_scales[self.frame]

        # Step 4: next frame for further animation
        self.frame += 1

        # Step 5: checking switch to the next phase
        if self.phase == PHASE.MOVING and self.frame >= self.fpp_moving:
            self._finish_moving()
            self._next_phase()
        if self.phase == PHASE.ARISING and self.frame >= self.fpp_arising:
            self._finish_arising()
            self._next_phase()
