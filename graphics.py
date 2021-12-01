# System imports
from os import environ, path

# External imports
import numpy as np
import pygame as pg
import pygame.gfxdraw

# Project imports
import config as c


class Graphics:
    """Setup of pygame graphics."""

    def __init__(self):

        # Setup pygame graphics
        environ['SDL_VIDEO_CENTERED'] = '1'  # centering pygame window
        pg.init()
        if c.SCREEN.FULL_SCREEN_MODE:
            self.screen = pg.display.set_mode(c.SCREEN.RESOLUTION, pg.FULLSCREEN)
        else:
            self.screen = pg.display.set_mode(c.SCREEN.RESOLUTION)

        # Taskbar appearance
        pg.display.set_caption('2048')
        pg.display.set_icon(pg.image.load(path.join('assets', 'favicon.ico')))

        self.draw_background()

        # preparing surfaces of tiles
        self.tiles = dict()
        self.prepare_tiles()

    def draw_background(self):
        """Drawing background to the screen surface."""
        self.screen.fill(pg.Color(c.GRID.COLOR))

    def prepare_tiles(self):
        """Pre-drawing all possible tiles for the game."""

        tiles_list = [0] + [2 << i for i in range((c.GAME.ROWS * c.GAME.COLS))]
        for tile in tiles_list:

            tile_surface = pg.Surface((c.TILE.SIZE, c.TILE.SIZE), pg.SRCALPHA)
            tile_rect = tile_surface.get_rect()

            pg.draw.rect(
                surface=tile_surface,
                color=c.TILE.COLOR.get(
                    tile,
                    c.TILE.COLOR_DEFAULT
                ),
                rect=tile_rect,
                border_radius=3
            )
            # pg.gfxdraw.box(
            #     tile_surface,
            #     tile_rect,
            #     pg.Color(c.TILE.COLOR.get(
            #         tile,
            #         c.TILE.COLOR_DEFAULT
            #     ))
            # )

            font_size_multiplier = c.TILE.SIZE_FACTOR ** (max(c.GAME.ROWS, c.GAME.COLS) - 4)
            font_size = int(c.TILE.FONT.SIZE.get(
                tile,
                c.TILE.FONT.SIZE_DEFAULT
            ) * font_size_multiplier)
            if tile:
                font = pg.font.Font(
                    path.join('assets', 'ClearSans-Bold.ttf'),
                    font_size
                )
                text = font.render(
                    str(tile),
                    True,
                    pg.Color(c.TILE.FONT.COLOR.get(
                        tile,
                        c.TILE.FONT.COLOR_DEFAULT
                    ))
                )
                text_rect = text.get_rect()
                text_rect.center = (c.TILE.SIZE // 2, c.TILE.SIZE // 2)
                tile_surface.blit(text, text_rect)

            self.tiles[tile] = tile_surface

    def draw_grid(self, matrix: np.ndarray):
        """Drawing figures on the screen."""

        rows, cols = matrix.shape
        for y in range(rows):
            for x in range(cols):

                try:
                    tile_surface = self.tiles[matrix[y, x]]
                except KeyError:
                    raise KeyError(f"Can't find predefined tile surface for the matrix value: {matrix[y, x]}")
                tile_rect = tile_surface.get_rect()
                tile_rect.center = (
                    c.SCREEN.X_TOP_LEFT + c.TILE.PADDING + x * (c.TILE.SIZE + c.TILE.PADDING) + c.TILE.SIZE // 2,
                    c.SCREEN.Y_TOP_LEFT + c.TILE.PADDING + y * (c.TILE.SIZE + c.TILE.PADDING) + c.TILE.SIZE // 2
                )

                self.screen.blit(tile_surface, tile_rect)

    @staticmethod
    def show():
        """Reflecting all the drawings on the display."""
        pg.display.flip()


# --- Graphics context realization --------------------------------------------

graphics = Graphics()
