# -----------------------------------------------------------------------------
# "2048" tribute to original https://2048game.com
# Copyright (c) Dec 2021 Oleksii Hurov
# -----------------------------------------------------------------------------

"""
(IV) Presentation level abstraction.
Graphics & UI provided by pygame & pygame_gui external modules.
"""


# System imports
from os import path

# External imports
import pygame as pg
import pygame_gui as pgui

# Project imports
from config import TILE, PANEL, SCREEN


# to avoid annoying console warning message from pygame_gui module
import warnings
warnings.filterwarnings('ignore', 'Label Rect is too small for text')


# --- GUI ---------------------------------------------------------------------

class GUI:
    """Setup pygame_gui."""

    def __init__(self, screen: pg.Surface):
        """Initializing pygame_gui graphics."""

        self.screen = screen
        self.resolution = self.screen.get_size()

        # Setup UI manager
        self.manager = pgui.UIManager(
            window_resolution = self.resolution,
            theme_path = path.join('assets', 'theme.json'),
            enable_live_theme_updates = False
        )

        self.panel_margins = {
            'top': 0,
            'left': 0,
            'right': 0,
            'bottom': 0
        }

        if PANEL.IS_PRESENT:
            self.create_panel()
            self.create_score()
            self.create_undo_button()
            self.create_new_game_button()

    def draw(self):
        """Drawing user interface to the screen surface."""
        self.manager.draw_ui(self.screen)

    # --- Defining UI Elements ------------------------------------------------

    def create_panel(self):
        """Creating operational panel with title label on it."""

        self.panel = pgui.elements.UIPanel(
            relative_rect = pg.Rect(
                PANEL.X_TOP_LEFT, PANEL.Y_TOP_LEFT,
                PANEL.WIDTH, PANEL.HEIGHT
            ),
            starting_layer_height = 1,
            manager = self.manager,
            margins = self.panel_margins
        )

        self.label_2048 = pgui.elements.UILabel(
            relative_rect = pg.Rect(8, -10, 246, 138),
            text = '2048',
            manager = self.manager,
            container = self.panel,
            object_id = 'label_2048',
            anchors = {
                'left': 'left',
                'right': 'left',
                'top': 'top',
                'bottom': 'top'
            }
        )

    def create_score(self):
        """Creating score panel with info labels on it."""

        panel_score_rect = pg.Rect(0, 0, 2 * TILE.SIZE_4x4 + TILE.PADDING_4x4, 70)
        panel_score_rect.topright = (PANEL.WIDTH - TILE.PADDING_4x4, 30)
        self.panel_score = pgui.elements.UIPanel(
            relative_rect = panel_score_rect,
            starting_layer_height = 2,
            manager = self.manager,
            margins = self.panel_margins,
            container = self.panel,
            object_id = 'panel_score'
        )

        label_score_rect = pg.Rect(0, 0, 0.9 * panel_score_rect.width, 22)
        label_score_rect.midtop = (panel_score_rect.width // 2, 8)
        self.label_score = pgui.elements.UILabel(
            relative_rect = label_score_rect,
            text = 'SCORE',
            manager = self.manager,
            container = self.panel_score,
            object_id = 'label_score'
        )

        label_score_value_rect = pg.Rect(0, 0, 0.9 * panel_score_rect.width, 44)
        label_score_value_rect.midtop = (panel_score_rect.width // 2, 24)
        self.label_score_value = pgui.elements.UILabel(
            relative_rect = label_score_value_rect,
            text = '0',
            manager = self.manager,
            container = self.panel_score,
            object_id = 'label_score_value'
        )

    def update_score(self, score: int):
        self.label_score_value.set_text(str(score))

    def create_undo_button(self):
        """Creating [Undo] button."""

        button_undo_rect = pg.Rect(0, 0, TILE.SIZE_4x4, 50)
        button_undo_rect.bottomleft = (
            TILE.PADDING_4x4,
            PANEL.HEIGHT - SCREEN.MARGIN
        )
        self.button_undo = pgui.elements.UIButton(
            relative_rect = button_undo_rect,
            text = 'Undo',
            manager = self.manager,
            container = self.panel
        )
        self.button_undo.hide()

    def create_new_game_button(self):
        """Creating [New Game] button."""

        button_new_game_rect = pg.Rect(0, 0, TILE.SIZE_4x4, 50)
        button_new_game_rect.bottomright = (
            PANEL.WIDTH - TILE.PADDING_4x4,
            PANEL.HEIGHT - SCREEN.MARGIN
        )
        self.button_new_game = pgui.elements.UIButton(
            relative_rect = button_new_game_rect,
            text = 'New Game',
            manager = self.manager,
            container = self.panel
        )

    def create_confirmation_dialog(self):
        # TODO

        self.panel_fader = pgui.elements.UIPanel(
            relative_rect = pg.Rect(
                SCREEN.X_TOP_LEFT, SCREEN.Y_TOP_LEFT,
                SCREEN.WIDTH, SCREEN.HEIGHT
            ),
            starting_layer_height = 4,
            manager = self.manager,
            margins = self.panel_margins,
            object_id = 'panel_fader'
        )

        confirmation_dialog_rect = pg.Rect(0, 0, 340, 100)
        confirmation_dialog_rect.midtop = (SCREEN.X_CENTER, 10)
        self.confirmation_dialog = pgui.windows.UIConfirmationDialog(
            rect = confirmation_dialog_rect,
            manager = self.manager,
            action_long_desc = 'Do you really want to start new game?',
            action_short_name = 'Yes'
        )
