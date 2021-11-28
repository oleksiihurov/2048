# System imports
from dataclasses import dataclass


@dataclass
class GRID:
    """
    Set of constants for game's Grid.
    """

    ROWS = 4  # min = 3; max = 20
    COLS = 4  # min = 3; max = 20
    WIN_TILE = 2048

    class COLOR:
        BACKGROUND = '#bbada0'


@dataclass
class TILE:
    """
    Set of constants for particular grid's Tile.
    """

    # base size in pixels for the smallest grid 3x3
    _BASE_SIZE = 130
    # multiplication factor for every larger grid
    _SIZE_FACTOR = 0.95
    # size in pixels based on number of Grid's rows/cols
    SIZE = int(_BASE_SIZE * _SIZE_FACTOR ** (max(GRID.ROWS, GRID.COLS) - 3))

    # multiplication factor from Tile's size
    _PADDING_MULTIPLIER = 0.12
    # size in pixels between Tiles
    PADDING = int(SIZE * _PADDING_MULTIPLIER)

    class COLOR:
        BACKGROUND = {
            0: '#cdc0b4',  # empty tile
            1: None,  # impossible tile
            2: '#eee4da',
            4: '#ede0c8',
            8: '#f2b179',
            16: '#f59563',
            32: '#f67c5f',
            64: '#f65e3b',
            128: '#edcf72',
            256: '#edcc61',
            512: '#edc850',
            1024: '#edc53f',
            2048: '#edc22e',
            4096: '#3c3a32',
            8192: '#3c3a32',
            16384: '#3c3a32',
            32768: '#3c3a32',
            65536: '#3c3a32',
        }
        FOREGROUND = {
            0: None,  # empty tile
            1: None,  # impossible tile
            2: '#776e65',
            4: '#776e65',
            8: '#f9f6f2',
            16: '#f9f6f2',
            32: '#f9f6f2',
            64: '#f9f6f2',
            128: '#f9f6f2',
            256: '#f9f6f2',
            512: '#f9f6f2',
            1024: '#f9f6f2',
            2048: '#f9f6f2',
            4096: '#f9f6f2',
            8192: '#f9f6f2',
            16384: '#f9f6f2',
            32768: '#f9f6f2',
            65536: '#f9f6f2',
        }


@dataclass
class SCREEN:
    """Set of constants for Screen."""

    # size of the Grid in pixels
    _GRID_WIDTH = GRID.COLS * TILE.SIZE + (GRID.COLS + 1) * TILE.PADDING
    _GRID_HEIGHT = GRID.ROWS * TILE.SIZE + (GRID.ROWS + 1) * TILE.PADDING

    # actual display fullscreen resolution do not considering OS scale and layout:
    # thanks to solution by
    # https://gamedev.stackexchange.com/questions/105750/pygame-fullsreen-display-issue
    import ctypes
    ctypes.windll.user32.SetProcessDPIAware()

    FULL_SCREEN_MODE = False

    if FULL_SCREEN_MODE:
        RESOLUTION = (
            ctypes.windll.user32.GetSystemMetrics(0),
            ctypes.windll.user32.GetSystemMetrics(1)
        )
    else:
        # calculating "window size" based on ROWS & COLS in ranges:
        # 300 <= width (px) <= 1280
        # 200 <= height (px) <= 760
        RESOLUTION = (
            max(300, min(1280, _GRID_WIDTH)),
            max(200, min(760, _GRID_HEIGHT))
        )

        # or manually set "window size":
        # RESOLUTION = (800, 600)

    # dimensions
    WIDTH, HEIGHT = RESOLUTION
    X_CENTER = WIDTH // 2
    Y_CENTER = HEIGHT // 2
    X_TOP_LEFT = X_CENTER - _GRID_WIDTH // 2
    Y_TOP_LEFT = Y_CENTER - _GRID_HEIGHT // 2

    # frames per second
    FPS = 60
