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
    SIZE_FACTOR = 0.95
    # size in pixels based on number of Grid's rows/cols
    SIZE = int(_SIZE_3x3 * SIZE_FACTOR ** (max(GAME.ROWS, GAME.COLS) - 3))

    # fraction from Tile's size
    _PADDING_FRACTION = 0.12
    # size in pixels between Tiles
    PADDING = int(SIZE * _PADDING_FRACTION)

    COLOR_DEFAULT = '#000000'
    COLOR = {
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

        131072: '#3c3a32',
        262144: '#3c3a32',
        524288: '#3c3a32',
        1048576: '#3c3a32',
        2097152: '#3c3a32',
        4194304: '#3c3a32',
        8388608: '#3c3a32',
        16777216: '#3c3a32',
        33554432: '#3c3a32',
        67108864: '#3c3a32',
        134217728: '#3c3a32',
        268435456: '#3c3a32',
        536870912: '#3c3a32',
        1073741824: '#3c3a32',
        2147483648: '#3c3a32',
        4294967296: '#3c3a32'
    }

    @dataclass
    class FONT:
        COLOR_DEFAULT = '#ffffff'
        COLOR = {
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

            131072: '#f9f6f2',
            262144: '#f9f6f2',
            524288: '#f9f6f2',
            1048576: '#f9f6f2',
            2097152: '#f9f6f2',
            4194304: '#f9f6f2',
            8388608: '#f9f6f2',
            16777216: '#f9f6f2',
            33554432: '#f9f6f2',
            67108864: '#f9f6f2',
            134217728: '#f9f6f2',
            268435456: '#f9f6f2',
            536870912: '#f9f6f2',
            1073741824: '#f9f6f2',
            2147483648: '#f9f6f2',
            4294967296: '#f9f6f2'
        }
        SIZE_DEFAULT = 25
        SIZE = {  # for the grid 4x4
            0: 65,  # empty tile
            2: 65,
            4: 65,
            8: 65,
            16: 65,
            32: 65,
            64: 65,
            128: 53,
            256: 53,
            512: 53,
            1024: 41,
            2048: 41,
            4096: 41,
            8192: 41,
            16384: 34,
            32768: 34,
            65536: 34,

            131072: 27,
            262144: 27,
            524288: 27,
            1048576: 24,
            2097152: 24,
            4194304: 24,
            8388608: 24,
            16777216: 20,
            33554432: 20,
            67108864: 20,
            134217728: 18,
            268435456: 18,
            536870912: 18,
            1073741824: 17,
            2147483648: 17,
            4294967296: 17
        }


@dataclass
class GRID:
    """
    Set of constants for Grid.
    """

    # size of the Grid in pixels
    WIDTH = GAME.COLS * TILE.SIZE + (GAME.COLS + 1) * TILE.PADDING
    HEIGHT = GAME.ROWS * TILE.SIZE + (GAME.ROWS + 1) * TILE.PADDING

    COLOR = '#bbada0'


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
