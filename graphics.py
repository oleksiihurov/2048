# System imports
from os import environ, path

# External imports
import numpy as np
import pygame as pg

# Project imports
from config import GAME, TILE, GRID, SCREEN, ANIMATION
from tiles import Tiles


# --- Graphics ----------------------------------------------------------------

class Graphics:
    """Setup of pygame graphics."""

    def __init__(self, resolution: tuple[int, int]):
        """Initializing pygame graphics."""

        # Initialization pygame display
        environ['SDL_VIDEO_CENTERED'] = '1'  # centering pygame window
        pg.init()
        if SCREEN.FULL_SCREEN_MODE:
            self.screen = pg.display.set_mode(resolution, pg.FULLSCREEN)
        else:
            self.screen = pg.display.set_mode(resolution)

        # Taskbar appearance
        pg.display.set_caption('2048')
        pg.display.set_icon(pg.image.load(path.join('assets', 'favicon.ico')))

        # Setup process
        self.clock = pg.time.Clock()
        self.time_delta = None

        # preparing surfaces of tiles
        self.tile_surfaces = dict()
        self.prepare_tiles()

        self.draw_screen_background()
        self.grid_background_surface_rect = self.draw_grid_background()

    def draw_screen_background(self):
        """Drawing background to the screen surface."""

        self.screen.fill(
            pg.Color(SCREEN.BG_COLOR),
            (0, 0, SCREEN.WIDTH, SCREEN.HEIGHT)
        )

    def draw_grid_background(self):
        """Drawing background for the grid."""

        grid_background_surface = pg.Surface(
            (GRID.WIDTH, GRID.HEIGHT),
            pg.SRCALPHA
        )

        pg.draw.rect(
            surface = grid_background_surface,
            color = pg.Color(GRID.BG_COLOR),
            rect = (
                0, 0,
                GRID.WIDTH, GRID.HEIGHT
            ),
            border_radius = 7
        )

        empty_tile_surface = self.tile_surfaces[0]

        for row in range(GAME.ROWS):
            for col in range(GAME.COLS):
                empty_tile_rect = empty_tile_surface.get_rect()
                empty_tile_rect.center = (
                    TILE.PADDING + TILE.SIZE // 2 +
                    col * (TILE.SIZE + TILE.PADDING),
                    TILE.PADDING + TILE.SIZE // 2 +
                    row * (TILE.SIZE + TILE.PADDING)
                )

                grid_background_surface.blit(
                    empty_tile_surface,
                    empty_tile_rect
                )

        grid_background_rect = grid_background_surface.get_rect()
        grid_background_rect.topleft = (
            GRID.X_TOP_LEFT,
            GRID.Y_TOP_LEFT
        )
        self.screen.blit(
            grid_background_surface,
            grid_background_rect
        )

        return grid_background_surface, grid_background_rect

    def clock_tick(self):
        """Ticking clock. Also calculating time_delta for GUI elements."""
        self.time_delta = self.clock.tick(ANIMATION.FPS) / 1000.0

    @staticmethod
    def show():
        """Reflecting all the drawings on the display."""
        pg.display.flip()

    # --- Grid drawings -------------------------------------------------------

    @staticmethod
    def get_tile_color(tile):
        try:
            result = TILE.COLOR[tile]
        except KeyError:
            result = TILE.COLOR[-1]
        return pg.Color(result)

    @staticmethod
    def get_tile_font_color(tile):
        try:
            result = TILE.FONT_COLOR[tile]
        except KeyError:
            result = TILE.FONT_COLOR[-1]
        return pg.Color(result)

    @staticmethod
    def get_tile_font_size(tile):
        try:
            result = TILE.FONT_SIZE_4x4[tile]
        except KeyError:
            result = TILE.FONT_SIZE_4x4[-1]
        return int(result * TILE.SCALE)

    @staticmethod
    def get_tile_value(tile):
        try:
            result = TILE.VALUE[tile]
        except KeyError:
            result = TILE.VALUE[-1]
        return result

    def prepare_tiles(self):
        """Pre-drawing all possible tiles for the game."""

        tiles_list = [0] + [i + 1 for i in range((GAME.ROWS * GAME.COLS))]
        for tile in tiles_list:

            tile_surface = pg.Surface((TILE.SIZE, TILE.SIZE), pg.SRCALPHA)
            tile_rect = tile_surface.get_rect()

            pg.draw.rect(
                surface = tile_surface,
                color = self.get_tile_color(tile),
                rect = tile_rect,
                border_radius = 3
            )

            # pg.draw.rect(
            #     surface = tile_surface,
            #     color = self.get_tile_font_color(tile),
            #     rect = tile_rect,
            #     width = 1,
            #     border_radius = 3
            # )

            if tile:
                font = pg.font.Font(
                    path.join('assets', 'ClearSansBold.ttf'),
                    self.get_tile_font_size(tile)
                )
                text = font.render(
                    self.get_tile_value(tile),
                    True,
                    self.get_tile_font_color(tile)
                )
                text_rect = text.get_rect()
                text_rect.center = (TILE.SIZE // 2, TILE.SIZE // 2)
                tile_surface.blit(text, text_rect)

            self.tile_surfaces[tile] = tile_surface

    def draw_grid(self, matrix: np.ndarray):
        """Drawing grid on the screen."""

        rows, cols = matrix.shape
        for row in range(rows):
            for col in range(cols):
                try:
                    tile_surface = self.tile_surfaces[matrix[row, col]]
                except KeyError:
                    raise KeyError(f"Can't find predefined tile surface"
                                   f" for the matrix value: {matrix[row, col]}")
                tile_rect = tile_surface.get_rect()
                tile_rect.center = (
                    GRID.X_TOP_LEFT + TILE.PADDING + TILE.SIZE // 2 +
                    col * (TILE.SIZE + TILE.PADDING),
                    GRID.Y_TOP_LEFT + TILE.PADDING + TILE.SIZE // 2 +
                    row * (TILE.SIZE + TILE.PADDING)
                )

                self.screen.blit(tile_surface, tile_rect)

    def animate_tiles(self, tiles: Tiles):
        """Animating tiles on the screen."""

        self.screen.blit(*self.grid_background_surface_rect)

        for tile in tiles:
            if tile.show:
                try:
                    tile_surface = self.tile_surfaces[tile.value]
                except KeyError:
                    raise KeyError(f"Can't find predefined tile surface"
                                   f" for the tile value: {tile.value}")
                if tile.scale != 1:
                    tile_surface = pg.transform.scale(
                        tile_surface,
                        (tile.scale * TILE.SIZE, tile.scale * TILE.SIZE)
                    )
                tile_rect = tile_surface.get_rect()
                tile_rect.center = (tile.x, tile.y)

                self.screen.blit(tile_surface, tile_rect)
