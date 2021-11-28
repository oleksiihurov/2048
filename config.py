# System imports
from dataclasses import dataclass


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

    # base size in pixels for the smallest grid 3x3
    _SIZE_3x3 = 130
    # multiplication factor for every larger grid
    _SIZE_FACTOR = 0.95
    # size in pixels based on number of Grid's rows/cols
    SIZE = int(_SIZE_3x3 * _SIZE_FACTOR ** (max(GAME.ROWS, GAME.COLS) - 3))

    # fraction from Tile's size
    _PADDING_FRACTION = 0.12
    # size in pixels between Tiles
    PADDING = int(SIZE * _PADDING_FRACTION)

    @dataclass
    class COLOR:
        BACKGROUND_DEFAULT = '#000000'
        BACKGROUND = {
            0: '#cdc0b4',  # empty tile
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
        FOREGROUND_DEFAULT = '#ffffff'
        FOREGROUND = {
            0: '#ffffff',  # empty tile
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
class GRID:
    """
    Set of constants for Grid.
    """

    # size of the Grid in pixels
    WIDTH = GAME.COLS * TILE.SIZE + (GAME.COLS + 1) * TILE.PADDING
    HEIGHT = GAME.ROWS * TILE.SIZE + (GAME.ROWS + 1) * TILE.PADDING

    @dataclass
    class COLOR:
        BACKGROUND = '#bbada0'


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
            max(200, min(MONITOR_HEIGHT - 60, GRID.HEIGHT))
        )
    # else:  # manually set window size
    #     RESOLUTION = (800, 600)

    # dimensions
    WIDTH, HEIGHT = RESOLUTION
    X_CENTER = WIDTH // 2
    Y_CENTER = HEIGHT // 2
    X_TOP_LEFT = X_CENTER - GRID.WIDTH // 2
    Y_TOP_LEFT = Y_CENTER - GRID.HEIGHT // 2

    # frames per second
    FPS = 60
