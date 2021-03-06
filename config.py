# -----------------------------------------------------------------------------
# "2048" tribute to original https://2048game.com
# Copyright (c) Dec 2021 Oleksii Hurov
# -----------------------------------------------------------------------------

"""
(II) Input level abstraction.
Predefined parameters, constants and types.
"""


# System imports
from dataclasses import dataclass
from os import path
import json
from enum import Enum, auto


@dataclass
class GAME:
    """Set of constants for Game."""

    # matrix size
    ROWS = 4  # 2 <= ROWS <= 16
    COLS = 4  # 2 <= COLS <= 16

    # number of available undo operations
    UNDO = 10  # 0 <= UNDO <= 10


@dataclass
class TILE:
    """Set of constants for particular Tile of the Grid."""

    # base size in pixels for the original grid 4x4
    SIZE_4x4 = 123
    # fraction from Tile's size
    PADDING_FRACTION = 0.12
    # size in pixels between Tiles
    PADDING_4x4 = int(SIZE_4x4 * PADDING_FRACTION)

    # size of the Tile in pixels
    SIZE = None  # will be calculated further
    PADDING = None  # will be calculated further
    SCALE = None  # will be calculated further

    # with open(path.join('assets', 'TileColorsAlternative.json'), 'r') as json_file:
    with open(path.join('assets', 'TileColors.json'), 'r') as json_file:
        obj = json.load(json_file)
    COLOR = {int(k): v for k, v in obj.items()}

    # with open(path.join('assets', 'TileFontColorsAlternative.json'), 'r') as json_file:
    with open(path.join('assets', 'TileFontColors.json'), 'r') as json_file:
        obj = json.load(json_file)
    FONT_COLOR = {int(k): v for k, v in obj.items()}

    # with open(path.join('assets', 'TileFontSizesAlternative.json'), 'r') as json_file:
    with open(path.join('assets', 'TileFontSizes.json'), 'r') as json_file:
        obj = json.load(json_file)
    FONT_SIZE_4x4 = {int(k): v for k, v in obj.items()}

    # with open(path.join('assets', 'TileValuesAlternative.json'), 'r') as json_file:
    with open(path.join('assets', 'TileValues.json'), 'r') as json_file:
        obj = json.load(json_file)
    VALUE = {int(k): v for k, v in obj.items()}


@dataclass
class GRID:
    """Set of constants for Grid of the Screen."""

    # base dimensions in pixels for the grid 4x4
    WIDTH_4x4 = 4 * TILE.SIZE_4x4 + 5 * TILE.PADDING_4x4
    HEIGHT_4x4 = 4 * TILE.SIZE_4x4 + 5 * TILE.PADDING_4x4

    # dimensions of the Grid in pixels
    WIDTH = None  # will be calculated further
    HEIGHT = None  # will be calculated further

    X_TOP_LEFT = None  # will be calculated further
    Y_TOP_LEFT = None  # will be calculated further

    BG_COLOR = '#bbada0'


@dataclass
class PANEL:
    """Set of constants for Operational Panel of the screen."""

    IS_PRESENT = True

    # size of the Operational Panel in pixels
    WIDTH = None  # will be calculated further
    HEIGHT = 194 if IS_PRESENT else 0

    X_TOP_LEFT = None  # will be calculated further
    Y_TOP_LEFT = None  # will be calculated further


@dataclass
class SCREEN:
    """Set of constants for Screen."""

    FULL_SCREEN_MODE = False

    # Actual display fullscreen resolution
    # do not considering OS scale and layout:
    # (thanks to solution by)
    # https://gamedev.stackexchange.com/questions/105750/pygame-fullsreen-display-issue
    import ctypes
    ctypes.windll.user32.SetProcessDPIAware()
    MONITOR_WIDTH = ctypes.windll.user32.GetSystemMetrics(0)
    MONITOR_HEIGHT = ctypes.windll.user32.GetSystemMetrics(1)

    WIDTH_MIN = 590
    HEIGHT_MIN = 200

    WIDTH_MAX = MONITOR_WIDTH if FULL_SCREEN_MODE else MONITOR_WIDTH - 100
    HEIGHT_MAX = MONITOR_HEIGHT if FULL_SCREEN_MODE else MONITOR_HEIGHT - 100

    # SCREEN dimensions
    WIDTH = None  # will be calculated further
    HEIGHT = None  # will be calculated further
    RESOLUTION = None  # will be calculated further

    MARGIN = 14

    X_CENTER = None  # will be calculated further
    Y_CENTER = None  # will be calculated further
    X_TOP_LEFT = None  # will be calculated further
    Y_TOP_LEFT = None  # will be calculated further

    BG_COLOR = '#faf8ef'


@dataclass
class ANIMATION:
    """Set of constants for Animation."""

    IS_PRESENT = True

    # frames per second
    FPS = 60

    # how much time it takes (in seconds) for each of animation stage
    TIME_MOVING = 0.1
    TIME_ARISING = 0.1


class MOVE(Enum):
    """Supported tile moves in the grid: up, down, right, left."""
    NONE = 0
    UP = auto()
    DOWN = auto()
    RIGHT = auto()
    LEFT = auto()


class PHASE(Enum):
    """Sequence of animation phases."""
    MOVING = auto()
    ARISING = auto()
    FINISH = auto()


# -----------------------------------------------------------------------------

def calculating_the_scale_multiplier():
    """
    Most of the constants from the TILE, GRID, PANEL, SCREEN classes
    left to be blank (None value) due to inability to define them right away.
    So we need to calculate them backwards, based on such predefined values
    for original Grid 4x4 - through the largest supported grid 16x16,
    and taking into account conditions from SCREEN and PANEL classes.
    """

    if not max(GAME.ROWS, GAME.COLS) == 4:
        # Step 1: calculating non-scaled maximum supported grid dimensions
        _TOTAL_WIDTH_16x16 = 16 * GRID.WIDTH_4x4 / 4 + 2 * SCREEN.MARGIN
        _TOTAL_HEIGHT_16x16 = 16 * GRID.HEIGHT_4x4 / 4 + PANEL.HEIGHT + SCREEN.MARGIN

        # Step 2: deciding which dimension is taken as size limit
        if _TOTAL_HEIGHT_16x16 / SCREEN.HEIGHT_MAX > _TOTAL_WIDTH_16x16 / SCREEN.WIDTH_MAX:
            _GRID_HEIGHT_16x16 = SCREEN.HEIGHT_MAX - PANEL.HEIGHT - SCREEN.MARGIN
            _GRID_WIDTH_16x16 = _GRID_HEIGHT_16x16
        else:
            _GRID_WIDTH_16x16 = SCREEN.WIDTH_MAX - 2 * SCREEN.MARGIN
            _GRID_HEIGHT_16x16 = _GRID_WIDTH_16x16

        # Step 3: calculating TILE.SIZE, taking the wider dimension as basement
        if GAME.COLS > GAME.ROWS:
            GRID.WIDTH = GRID.WIDTH_4x4 + (GAME.COLS - 4) * (_GRID_WIDTH_16x16 - GRID.WIDTH_4x4) / (16 - 4)
            # GRID.WIDTH == GAME.COLS * TILE.SIZE + (GAME.COLS + 1) * int(TILE.SIZE * TILE.PADDING_FRACTION)
            TILE.SIZE = int(GRID.WIDTH / (GAME.COLS + (GAME.COLS + 1) * TILE.PADDING_FRACTION))
        else:
            GRID.HEIGHT = GRID.HEIGHT_4x4 + (GAME.ROWS - 4) * (_GRID_HEIGHT_16x16 - GRID.HEIGHT_4x4) / (16 - 4)
            # GRID.HEIGHT == GAME.ROWS * TILE.SIZE + (GAME.ROWS + 1) * int(TILE.SIZE * TILE.PADDING_FRACTION)
            TILE.SIZE = int(GRID.HEIGHT / (GAME.ROWS + (GAME.ROWS + 1) * TILE.PADDING_FRACTION))

    else:  # grid size == 4
        TILE.SIZE = TILE.SIZE_4x4  # to avoid rounding error

    # Step 4: recalculating GRID dimensions according to rounded TILE.SIZE
    TILE.PADDING = int(TILE.SIZE * TILE.PADDING_FRACTION)
    GRID.WIDTH = GAME.COLS * TILE.SIZE + (GAME.COLS + 1) * TILE.PADDING
    GRID.HEIGHT = GAME.ROWS * TILE.SIZE + (GAME.ROWS + 1) * TILE.PADDING

    # Step 5: calculating the TILE.SCALE multiplier
    TILE.SCALE = TILE.SIZE / TILE.SIZE_4x4

    # Step 6: calculating the rest of the dimensions
    PANEL.WIDTH = max(SCREEN.WIDTH_MIN - 2 * SCREEN.MARGIN, GRID.WIDTH)

    if SCREEN.FULL_SCREEN_MODE:
        SCREEN.RESOLUTION = (
            SCREEN.MONITOR_WIDTH,
            SCREEN.MONITOR_HEIGHT
        )
    else:  # WINDOW_MODE
        SCREEN.RESOLUTION = (
            max(SCREEN.WIDTH_MIN, min(SCREEN.WIDTH_MAX, GRID.WIDTH + 2 * SCREEN.MARGIN)),
            max(SCREEN.HEIGHT_MIN, min(SCREEN.HEIGHT_MAX, GRID.HEIGHT + PANEL.HEIGHT + SCREEN.MARGIN))
        )

    SCREEN.WIDTH, SCREEN.HEIGHT = SCREEN.RESOLUTION

    SCREEN.X_CENTER = SCREEN.WIDTH // 2
    SCREEN.Y_CENTER = SCREEN.HEIGHT // 2
    SCREEN.X_TOP_LEFT = SCREEN.X_CENTER - (GRID.WIDTH + 2 * SCREEN.MARGIN) // 2
    SCREEN.Y_TOP_LEFT = SCREEN.Y_CENTER - (PANEL.HEIGHT + GRID.HEIGHT + SCREEN.MARGIN) // 2

    # PANEL.X_TOP_LEFT = SCREEN.X_TOP_LEFT + SCREEN.MARGIN
    PANEL.X_TOP_LEFT = SCREEN.X_CENTER - PANEL.WIDTH // 2
    PANEL.Y_TOP_LEFT = SCREEN.Y_TOP_LEFT

    GRID.X_TOP_LEFT = SCREEN.X_TOP_LEFT + SCREEN.MARGIN
    GRID.Y_TOP_LEFT = SCREEN.Y_TOP_LEFT + PANEL.HEIGHT


# -----------------------------------------------------------------------------

calculating_the_scale_multiplier()
