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
        if c.PANEL1.IS_PRESENT:
            self.draw_panel1()

        # preparing surfaces of tiles
        self.tiles = dict()
        self.prepare_tiles()

    def draw_background(self):
        """Drawing background to the screen surface."""

        # self.screen.fill(pg.Color(c.GRID.BG_COLOR))
        self.screen.fill(
            pg.Color(c.PANEL1.BG_COLOR),
            (c.PANEL1.X_TOP_LEFT, c.PANEL1.Y_TOP_LEFT, c.PANEL1.WIDTH, c.PANEL1.HEIGHT)
        )
        self.screen.fill(
            pg.Color(c.GRID.BG_COLOR),
            (c.GRID.X_TOP_LEFT, c.GRID.Y_TOP_LEFT, c.GRID.WIDTH, c.GRID.HEIGHT)
        )

    @staticmethod
    def show():
        """Reflecting all the drawings on the display."""
        pg.display.flip()

    # --- Panel drawings ------------------------------------------------------

    def draw_button(self, button_text: str, topright_position):
        button_surface = pg.Surface((c.TILE.SIZE, 40), pg.SRCALPHA)
        button_rect = button_surface.get_rect()

        pg.draw.rect(
            surface=button_surface,
            color=pg.Color(c.PANEL1.BUTTON_COLOR),
            rect=button_rect,
            border_radius=3
        )

        font_size_multiplier = c.TILE.SIZE_FACTOR ** (max(c.GAME.ROWS, c.GAME.COLS) - 4)
        font_size = int(c.PANEL1.BUTTON_FONT_SIZE * font_size_multiplier)
        font = pg.font.Font(
            path.join('assets', 'ClearSansBold.ttf'),
            font_size
        )
        text = font.render(
            button_text,
            True,
            pg.Color(c.PANEL1.BUTTON_FONT_COLOR)
        )
        text_rect = text.get_rect()
        text_rect.center = (c.TILE.SIZE // 2, 40 // 2)

        button_surface.blit(text, text_rect)
        button_rect.topright = topright_position

        self.screen.blit(button_surface, button_rect)

    def draw_label(self, label_text: str, width, height, label_color, label_font_color, label_font_size, topleft_position, text_center_alignment = True):
        label_surface = pg.Surface((width, height), pg.SRCALPHA)
        label_rect = label_surface.get_rect()

        pg.draw.rect(
            surface=label_surface,
            color=pg.Color(label_color),
            rect=label_rect,
            border_radius=3
        )

        font_size_multiplier = c.TILE.SIZE_FACTOR ** (max(c.GAME.ROWS, c.GAME.COLS) - 4)
        font_size = int(label_font_size * font_size_multiplier)
        font = pg.font.Font(
            path.join('assets', 'ClearSansBold.ttf'),
            font_size
        )
        text = font.render(
            label_text,
            True,
            pg.Color(label_font_color)
        )
        text_rect = text.get_rect()
        if text_center_alignment:
            text_rect.center = (width // 2, height // 2)
        else:
            text_rect.midleft = (0, height // 2)

        label_surface.blit(text, text_rect)
        label_rect.topleft = topleft_position

        self.screen.blit(label_surface, label_rect)

    def draw_score(self, score: int):
        if c.PANEL1.IS_PRESENT:
            self.draw_label(
                str(score),
                c.TILE.SIZE, 40,
                c.PANEL1.LABEL_COLOR,
                c.PANEL1.LABEL_VALUE_FONT_COLOR,
                c.PANEL1.LABEL_VALUE_FONT_SIZE,
                (c.PANEL1.X_TOP_LEFT + c.TILE.PADDING + c.TILE.SIZE // 1.1, c.PANEL1.Y_TOP_LEFT + 20),
                text_center_alignment=False
            )

    def draw_merged_tiles(self):
        if c.PANEL1.IS_PRESENT:
            pass
            # TODO

    def draw_panel1(self):
        """Drawing operational panel on the screen."""

        self.draw_button('New Game', (c.PANEL1.X_TOP_LEFT + c.PANEL1.WIDTH - c.TILE.PADDING, c.PANEL1.Y_TOP_LEFT + 20))
        self.draw_button('Undo', (c.PANEL1.X_TOP_LEFT + c.PANEL1.WIDTH - c.TILE.PADDING, c.PANEL1.Y_TOP_LEFT + 80))

        self.draw_label(
            'SCORE:',
            c.TILE.SIZE, 40,
            c.PANEL1.LABEL_COLOR,
            c.PANEL1.LABEL_FONT_COLOR,
            c.PANEL1.LABEL_FONT_SIZE,
            (c.PANEL1.X_TOP_LEFT + c.TILE.PADDING, c.PANEL1.Y_TOP_LEFT + 20)
        )
        self.draw_score(0)

    # --- Grid drawings -------------------------------------------------------

    @staticmethod
    def get_tile_color(tile):
        try:
            result = c.TILE.COLOR[tile]
        except KeyError:
            result = c.TILE.COLOR[-1]
        return pg.Color(result)

    @staticmethod
    def get_tile_font_color(tile):
        try:
            result = c.TILE.FONT_COLOR[tile]
        except KeyError:
            result = c.TILE.FONT_COLOR[-1]
        return pg.Color(result)

    @staticmethod
    def get_tile_font_size(tile):
        try:
            result = c.TILE.FONT_SIZE[tile]
        except KeyError:
            result = c.TILE.FONT_SIZE[-1]
        font_size_multiplier = c.TILE.SIZE_FACTOR ** (max(c.GAME.ROWS, c.GAME.COLS) - 4)
        return int(result * font_size_multiplier)

    def prepare_tiles(self):
        """Pre-drawing all possible tiles for the game."""

        tiles_list = [0] + [2 << i for i in range((c.GAME.ROWS * c.GAME.COLS))]
        for tile in tiles_list:

            tile_surface = pg.Surface((c.TILE.SIZE, c.TILE.SIZE), pg.SRCALPHA)
            tile_rect = tile_surface.get_rect()

            pg.draw.rect(
                surface=tile_surface,
                color=self.get_tile_color(tile),
                rect=tile_rect,
                border_radius=3
            )
            # pg.gfxdraw.box(
            #     tile_surface,
            #     tile_rect,
            #     self.get_tile_color(tile)
            # )

            if tile:
                font = pg.font.Font(
                    path.join('assets', 'ClearSansBold.ttf'),
                    self.get_tile_font_size(tile)
                )
                text = font.render(
                    str(tile),
                    True,
                    self.get_tile_font_color(tile)
                )
                text_rect = text.get_rect()
                text_rect.center = (c.TILE.SIZE // 2, c.TILE.SIZE // 2)
                tile_surface.blit(text, text_rect)

            self.tiles[tile] = tile_surface

    def draw_grid(self, matrix: np.ndarray):
        """Drawing grid on the screen."""

        rows, cols = matrix.shape
        for y in range(rows):
            for x in range(cols):

                try:
                    tile_surface = self.tiles[matrix[y, x]]
                except KeyError:
                    raise KeyError(f"Can't find predefined tile surface for the matrix value: {matrix[y, x]}")
                tile_rect = tile_surface.get_rect()
                tile_rect.center = (
                    c.GRID.X_TOP_LEFT + c.TILE.PADDING + x * (c.TILE.SIZE + c.TILE.PADDING) + c.TILE.SIZE // 2,
                    c.GRID.Y_TOP_LEFT + c.TILE.PADDING + y * (c.TILE.SIZE + c.TILE.PADDING) + c.TILE.SIZE // 2
                )

                self.screen.blit(tile_surface, tile_rect)


# --- Graphics context realization --------------------------------------------

graphics = Graphics()
