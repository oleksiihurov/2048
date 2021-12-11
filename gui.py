# System imports
from os import path

# External imports
import pygame as pg
import pygame_gui as pgui

# Project imports
from config import PANEL


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

        # padding in pixels between UI Elements
        self.gap = 0
        # margins in pixels for panel groups of UI Elements
        self.panel_margins = {
            'top': self.gap,
            'left': self.gap,
            'right': self.gap,
            'bottom': self.gap
        }

        self.create_panel()

    def draw(self):
        """Drawing user interface to the screen surface."""
        self.manager.draw_ui(self.screen)

    # --- Defining UI Elements ------------------------------------------------

    def create_panel(self):
        """Creating operational panel with info labels on it."""

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
            relative_rect = pg.Rect(10, 10, 200, 100),
            text = '2048',
            manager = self.manager,
            container = self.panel,
            object_id = 'label_2048'
        )
