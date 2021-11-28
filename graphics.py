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

    def draw_background(self):
        """Drawing background to the screen surface."""
        self.screen.fill(pg.Color(c.GRID.COLOR))

    def draw_grid(self, matrix: np.ndarray):
        """Drawing figures on the screen."""

        rows, cols = matrix.shape
        for y in range(rows):
            for x in range(cols):

                tile_rect = (
                    c.SCREEN.X_TOP_LEFT + c.TILE.PADDING + x * (c.TILE.SIZE + c.TILE.PADDING),
                    c.SCREEN.Y_TOP_LEFT + c.TILE.PADDING + y * (c.TILE.SIZE + c.TILE.PADDING),
                    c.TILE.SIZE,
                    c.TILE.SIZE
                )
                # pg.gfxdraw.box(
                #     self.screen,
                #     tile_rect,
                #     pg.Color(c.TILE.COLOR.get(
                #         matrix[y, x],
                #         c.TILE.COLOR_DEFAULT
                #     ))
                # )
                pg.draw.rect(
                    surface=self.screen,
                    color=c.TILE.COLOR.get(
                        matrix[y, x],
                        c.TILE.COLOR_DEFAULT
                    ),
                    rect=tile_rect,
                    border_radius=3
                )

                if matrix[y, x]:
                    font = pg.font.Font(
                        path.join('assets', 'ClearSans-Bold.ttf'),
                        c.TILE.FONT.SIZE.get(
                            matrix[y, x],
                            c.TILE.FONT.SIZE_DEFAULT
                        )
                    )
                    text = font.render(
                        str(matrix[y, x]),
                        True,
                        pg.Color(c.TILE.FONT.COLOR.get(
                            matrix[y, x],
                            c.TILE.FONT.COLOR_DEFAULT
                        ))
                    )
                    text_rect = text.get_rect()
                    text_rect.center = (
                        c.SCREEN.X_TOP_LEFT + c.TILE.PADDING + x * (c.TILE.SIZE + c.TILE.PADDING) + c.TILE.SIZE // 2,
                        c.SCREEN.Y_TOP_LEFT + c.TILE.PADDING + y * (c.TILE.SIZE + c.TILE.PADDING) + c.TILE.SIZE // 2
                    )
                    self.screen.blit(text, text_rect)

    @staticmethod
    def show():
        """Reflecting all the drawings on the display."""
        pg.display.flip()


# --- Graphics context realization --------------------------------------------

graphics = Graphics()
