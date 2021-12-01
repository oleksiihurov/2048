# System imports
from dataclasses import dataclass
from os import path
import json


@dataclass
class GAME:
    """
    Set of constants for Game.
    """

    ROWS = 4  # 3 <= ROWS <= 20
    COLS = 4  # 3 <= COLS <= 20
    WIN_TILE = 2048


@dataclass
class TILE:
    """
    Set of constants for particular Tile of Grid.
    """

    # base size in pixels for the grid 4x4
    _SIZE_4x4 = 123
    # multiplication factor for every larger grid
    SIZE_FACTOR = 0.95
    # size in pixels based on number of Grid's rows/cols
    SIZE = int(_SIZE_4x4 * SIZE_FACTOR ** (max(GAME.ROWS, GAME.COLS) - 4))

    # fraction from Tile's size
    _PADDING_FRACTION = 0.12
    # size in pixels between Tiles
    PADDING = int(SIZE * _PADDING_FRACTION)

    # with open(path.join('assets', 'TileColorsAlternative.json'), 'r') as json_file:
    with open(path.join('assets', 'TileColors.json'), 'r') as json_file:
        obj = json.load(json_file)
    COLOR = {int(k): v for k, v in obj.items()}

    # with open(path.join('assets', 'TileFontColorsAlternative.json'), 'r') as json_file:
    with open(path.join('assets', 'TileFontColors.json'), 'r') as json_file:
        obj = json.load(json_file)
    FONT_COLOR = {int(k): v for k, v in obj.items()}

    with open(path.join('assets', 'TileFontSizes.json'), 'r') as json_file:
        obj = json.load(json_file)
    FONT_SIZE = {int(k): v for k, v in obj.items()}


@dataclass
class GRID:
    """
    Set of constants for Grid.
    """

    # size of the Grid in pixels
    WIDTH = GAME.COLS * TILE.SIZE + (GAME.COLS + 1) * TILE.PADDING
    HEIGHT = GAME.ROWS * TILE.SIZE + (GAME.ROWS + 1) * TILE.PADDING

    # dimensions - should be redefined in SCREEN
    X_TOP_LEFT = 0
    Y_TOP_LEFT = 0

    BG_COLOR = '#bbada0'


@dataclass
class PANEL1:
    """
    Set of constants for Operational Panel.
    """

    IS_PRESENT = True

    # size of the Operational Panel in pixels
    WIDTH = GRID.WIDTH
    HEIGHT = 140 if IS_PRESENT else 0

    # dimensions - should be redefined in SCREEN
    X_TOP_LEFT = 0
    Y_TOP_LEFT = 0

    BG_COLOR = '#ffffff'

    BUTTON_COLOR = '#8f7a66'
    BUTTON_FONT_COLOR = '#ffffff'
    BUTTON_FONT_SIZE = 20

    LABEL_COLOR = GRID.BG_COLOR
    LABEL_FONT_COLOR = '#ffffff'
    LABEL_FONT_SIZE = 18
    LABEL_VALUE_FONT_COLOR = '#ffffff'
    LABEL_VALUE_FONT_SIZE = 26


@dataclass
class SCREEN:
    """Set of constants for Screen."""

    FULL_SCREEN_MODE = False

    # actual display fullscreen resolution do not considering OS scale and layout:
    # thanks to solution by
    # https://gamedev.stackexchange.com/questions/105750/pygame-fullsreen-display-issue
    import ctypes
    ctypes.windll.user32.SetProcessDPIAware()
    MONITOR_WIDTH = ctypes.windll.user32.GetSystemMetrics(0)
    MONITOR_HEIGHT = ctypes.windll.user32.GetSystemMetrics(1)

    if FULL_SCREEN_MODE:
        RESOLUTION = (
            MONITOR_WIDTH,
            MONITOR_HEIGHT
        )
    else:  # window size
        RESOLUTION = (
            max(300, min(MONITOR_WIDTH - 10, GRID.WIDTH)),
            max(200, min(MONITOR_HEIGHT - 60, PANEL1.HEIGHT + GRID.HEIGHT))
        )
    # else:  # manually set window size
    #     RESOLUTION = (800, 600)

    # SCREEN dimensions
    WIDTH, HEIGHT = RESOLUTION
    X_CENTER = WIDTH // 2
    Y_CENTER = HEIGHT // 2
    X_TOP_LEFT = X_CENTER - GRID.WIDTH // 2
    Y_TOP_LEFT = Y_CENTER - (PANEL1.HEIGHT + GRID.HEIGHT) // 2

    if PANEL1.IS_PRESENT:
        # redefining PANEL1 dimensions
        PANEL1.X_TOP_LEFT = X_TOP_LEFT
        PANEL1.Y_TOP_LEFT = Y_TOP_LEFT
        # redefining GRID dimensions
        GRID.X_TOP_LEFT = X_TOP_LEFT
        GRID.Y_TOP_LEFT = Y_TOP_LEFT + PANEL1.HEIGHT

    # frames per second
    FPS = 60
